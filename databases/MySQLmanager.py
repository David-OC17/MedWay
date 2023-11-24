'''
Here we provide a class to interact witht the MySQL database set up on AWS RDS.
The class has the functionality necesarry to:
* Create the tables in the database ('sensor data', 'batch alerts' and 'batch position' tables)
* Push new incoming data (raw) to 'sensor data' table
* Push to 'batch alerts' based on simple conditions of the raw data
* Push raw data to 'batch position'
* Query all three tables

The manager may receive information (sensor data) 24/7 and pools it in a local MySQL database.
The pool is uploaded and cleaned every 30 minutes, building up to 48 pushes every day.
This is done to reduce the number of connections and disconnections to the AWS server.

To create a manager for the local database, use 'local' managerType in constructor, else use 'cloud'
or 'aws' option for a cloud database manager.
'''

import mysql.connector
from mysql.connector import Error
from datetime import date, datetime,timedelta
from mysql.connector import connect
from time import strftime, time
from allQueryResult import QueryResult
import pandas as pd
import serial
from dotenv import load_dotenv
import csv
import os


from config import Config

load_dotenv()

class MySQLmanager:
    def send_to_cloud(self):
        # Set the time duration to 30 minutes (in seconds)
        duration = 30 * 60

        # Check if the current time has exceeded the start time + duration
        if time() - self.__start_time > duration:
            self.__start_time = time()
            return True
        
        return False
    
    def make_csv(self):
        # Set the time duration to 24 hours (in hours)
        duration = 24*60*60

        # Check if the current time has exceeded the start time + duration
        if time() - self.__start_time2 > duration:
            self.__start_time2 = time()
            return True
        
        return False
            
    def __init__(self, managerType: str) -> None:
        '''
        managerType: 'cloud' = 'aws' or 'local'
            or 'local_test' for testing
        '''
        if(managerType == 'cloud' or managerType == 'aws'):
            self.managerType = managerType
            self.db_config = {
                'host': os.getenv("CLOUD_HOST"),
                'user': os.getenv("CLOUD_USER"),
                'password': os.getenv("CLOUD_PASSWORD"),
                'database': os.getenv("CLOUD_DATABASE")
            }
        elif (managerType == 'local'):
            self.managerType = managerType
            self.db_config = {
                'host': os.getenv("LOCAL_HOST"),
                'user': os.getenv("LOCAL_USER"),
                'password': os.getenv("LOCAL_PASSWORD"),
                'database': os.getenv("LOCAL_DATABASE")
            }
        # elif (managerType == 'local_test'):
        #     self.managerType = managerType
        #     self.db_config = {
        #         'host': os.getenv("TEST_HOST"),
        #         'user': os.getenv("TEST_USER"),
        #         'password': os.getenv("TEST_PASSWORD"),
        #         'database': os.getenv("TEST_DATABASE")
        #     }
        else:
            raise ValueError("No suitable manager type for constructor of MySQLmanager. Use 'cloud' or 'local'.")
        
        #Get the times for the send and csv generator timing
        self.__start_time = time()
        self.__start_time2 = time()

    #################### START -> Create sensor table ####################
        self.create_sensor_data_table()
        
    def create_sensor_data_table(self) -> None:
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            create_sensor_data_query = """
            CREATE TABLE IF NOT EXISTS sensor_data (
                ID INT PRIMARY KEY AUTO_INCREMENT,
                batch_number INT,
                device_number INT,
                date DATE,
                time TIME,
                x_coordinate FLOAT,
                y_coordinate FLOAT,
                temperature FLOAT,
                humidity FLOAT,
                light_percentage FLOAT
            );
            """
            cursor.execute(create_sensor_data_query)
            connection.commit()
            print("Sensor Data table created successfully.")        
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    #################### END -> Create tables and stablish relationship ####################
    
    def fetch_data_from_database(self, start_id:int , end_id:int) -> list:
        '''
        Get a range of rows of values from the local database. Query the range given by startID-endID.
        Returns a list of values.
        '''
        if self.managerType != 'local':
                raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
            
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()

            # Query to fetch data within the specified ID range
            select_query = """
            SELECT batch_number,device_number,date,time,x_coordinate,y_coordinate,temperature,humidity,light_percentage
            FROM sensor_data
            WHERE ID BETWEEN %s AND %s
            """
            cursor.execute(select_query, (start_id, end_id))

            data_list = []
            for row in cursor.fetchall():
                # Append each row as a tuple to the data list
                data_list.append(row)

            return data_list # Return the tuple
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()  
    
    #################### START -> Push to cloud ####################

    def pushSensorData(self, starID: int, endID: int) -> None:
        '''
        Takes data from local sensor data table from startID to endID and pushes it to the cloud.
        Returns if upload was successful.
        '''        
        # Push all lines into the remote table
        if self.managerType != 'cloud':
                raise ValueError('Only cloud manager can interact with RDS cloud. Create a cloud manager to access.')
        try:

            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Define the INSERT INTO query with placeholders for data
            insert_query = """
            INSERT INTO sensor_data (batch_number,device_number,date,time, x_coordinate,y_coordinate,temperature,humidity,light_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s ,%s ,%s);
            """
            
            # Execute the query with data_list as a list of tuples
            data_list = local.fetch_data_from_database(starID, endID)
            cursor.executemany(insert_query, data_list)
            
            connection.commit()
            print("Records inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
            
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    #################### END -> Push to cloud ####################
    
    #################### START -> Delete from local ####################
    # Use this methods in order to delete the uploaded data from the local database
    def removeSensorData(self, startID: int, endID: int) -> None:
        '''
        Remove the sensor data in the range given by startID-endID.
        Use it to clean local database and avoid data cloning local-cloud.
        Return if the removal was successfull.
        '''
        if self.managerType != 'local':
            raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
        
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            delete_query = f"DELETE FROM sensor_data WHERE id >= {startID} AND id <= {endID}"
            
            cursor.execute(delete_query)
            
            connection.commit()
            print("Range of rows deleted successfully from sensor data.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def clearDatabase(self, confirmation:str='') -> None:
        '''
        Clear local/test database.
        Requires confirmation word 'DELETE ME' to perform the operation.
        Only meant for testing.
        '''
        # Ask for confirmation to clear the database
        if confirmation != 'DELETE ME':
            print('Confirmation not received, not clearing the database.')
        elif self.managerType != 'local_test':
            print('You can only clear all the database during testing and with a local_test manager.')
        
        confirmation = input('This a destructive action. To confirm, enter Y/y and enter. Any other characters cancel the operation.')
        if confirmation != 'Y' or confirmation != 'n':
            print('Database clearance cancelled.')
        
        # Proceed with clearing the database
            connection = mysql.connector.connect(**self.db_config)
            
            cursor = connection.cursor()
    
        try:
            # Get a list of all tables in the database
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            # Generate and execute DROP TABLE statements for each table
            for table in tables:
                table_name = table[0]
                drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
                cursor.execute(drop_table_query)
                print(f"Dropped table: {table_name}")

            # Commit the changes
            connection.commit()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()
        
    #################### END -> Delete from local ####################
    
    #################### START -> query tables ####################
    '''
    Provides the ability to query all tables all at once for a given date range or batch number.
    '''
    
    # def queryAllByDate(self, startDate:date, endDate:date) -> QueryResult:
    #     '''
    #     query cloud database for all the data corresponding to the given dates.
    #     Return a class queryResult with numpy arrays with the information.
    #     '''
    #     if self.managerType != 'cloud':
    #         raise ValueError('Only cloud manager can interact with RDS cloud. Create a cloud manager to access.')

        
    #     # The function connect to the cloud and makes two queries, one for the sensor data table and one for the batch alerts table
    #     # It generates a QueryResult type where it stores the query result
    #     try:
    #         # Convert startDate and endDate to MySQL type for query
    #         startDate = datetime.strptime(startDate, "%d%b%Y")
    #         mysql_startDate = startDate.strftime("%Y-%m-%d")
            
    #         endDate = datetime.strptime(endDate, "%d%b%Y")
    #         mysql_endDate = startDate.strftime("%Y-%m-%d")
        
            
    #         # Define query where date between startDate and endDate
    #         select_query = f"SELECT * FROM sensor_data WHERE date >= {mysql_startDate} AND date <= {mysql_endDate};"
                              
    #         cursor.execute(select_query)
            

    #         # '''
    #         # self.sensor_data_dtype =  np.dtype([
    #         #     ('ID', np.int64),
    #         #     ('batch_number', np.int64),
    #         #     ('device_number', np.int64),
    #         #     ('date', 'datetime64[D]'),  # Using datetime64[D] for date
    #         #     ('temperature', np.float64),
    #         #     ('humidity', np.float64),
    #         #     ('light_percentage', np.float64),
    #         #     ('time', 'timedelta64[s]'),  # Using timedelta64[s] for time
    #         #     ('x_coordinate', np.float64),
    #         #     ('y_coordinate', np.float64)
    #         # ])
            
    #         # '''
    #         # sensor_data_df = pd.DataFrame(cursor.fetchall())
    #         # result = QueryResult()
    #     except Error as e:
    #         print(f"Error: {e}")
    #     finally:
    #         if connection.is_connected():
    #             cursor.close()
    #             connection.close()
    
    #################### END -> query tables ####################

    #################### START -> Parse and add to local ####################
    
    # def parseAdd_TEST(self) -> None:
    #     '''
    #     TEST METHOD, DO NOT USE DURING PRODUCTION
    #     Receives a string of data, which is the incoming serial flow from the sensoring module.
    #     Parse the data and add it to the corresponding local database and tables.
    #     '''
        
    #     if self.managerType != 'local_test':
    #         raise ValueError('Local or cloud managers cannot alter test database. Create test manager to modify test_db.')
        
    #     df = pd.read_csv('../data/test_data.csv')

    #     # Extract data for temperature, humidity, and light
    #     temperature = df['temperature']
    #     humidity = df['humidity']
    #     light = df['light_percentage']
        
    #     # Establish connection to test_db
    #     local_connection: MySQLConnection = connect(**self.db_config)
        
    #     local_cursor: MySQLCursor = local_connection.cursor()
    #     print("Connected to test database!")
        
    #     # Recursively add data to test_db, simulating data entering from the incoming serial data
    #     for row in df:
    #         # Make a query
    #         print()
            
    #     local_cursor.close()
    #     local_connection.close()        

    #################### END -> Parse and add to local ####################

    #################### START -> CSV Generator ####################

    def csv_generator(self) -> None:
        
        if self.managerType != 'cloud':
            raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
        try:
            print("Generating CSV file...")
            header = ['ID','batch_number','device_number','date','time','x_coordinate','y_coordinate','temperature','humidity','light_percentage']
            
            # Get the previous date
            current_date = datetime.today()
            previous_Date = current_date - timedelta(days=1)   

            # Open the CSV file in write mode
            with open('./analysis/temp/tempData.csv', 'w', newline='') as tempData:
                csvwriter = csv.writer(tempData)
                csvwriter.writerow(header)

                # Connect to the MySQL database
                connection = mysql.connector.connect(**self.db_config)
                cursor = connection.cursor()

                # Convert startDate and endDate to MySQL type for query
                startDate = previous_Date
                mysql_startDate = startDate.strftime("%Y-%m-%d")

                endDate = previous_Date
                mysql_endDate = endDate.strftime("%Y-%m-%d")

                # Define and execute the SELECT query
                select_query = f"SELECT * FROM sensor_data WHERE date >= '{mysql_startDate}' AND date <= '{mysql_endDate}';"
                cursor.execute(select_query)
                
                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Write the rows to the CSV file
                for row in rows:
                    csvwriter.writerow(row)
        
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("CSV file generated successfully.")

    #################### END -> CSV Generator ####################

    #################### START -> Main functionality of manager ####################
    
    def receiver(self) -> None:
        '''
        Run when using 'local' manager in order to listen for incoming data streams to be stored in local database (later to be pushed to cloud)
        '''  
        if self.managerType != 'local':
            raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')

        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            print("Connected to local database")

            #Open a serial port that is connected to an Arduino
            #Program will wait until all serial data is received from Arduino
            #Port description will vary according to operating system. Linux will be in the form /dev/ttyXXXX and Windows and MAC will be COMX.
            
            port = serial.Serial(port='COM3', baudrate=9600)
            if port.isOpen() == False:
                port.open()
            #Write out a single character encoded in utf-8; this is defalt encoding for Arduino serial comms
            #This character tells the Arduino to start sending data
            port.write(bytes('x','utf-8'))
            while True:
        #Read in data from Serial until (new line) received
                port_bytes = port.readline()
            
                #Convert received bytes to text format and take out the new line characters and spaces 
                decoded_bytes = (port_bytes[0:len(port_bytes)-2].decode("utf-8").strip('\r\n\n'))
                
                #Retreive current time and date
                c = datetime.now()
                current_time = c.strftime('%H:%M:%S')
                current_date = c.strftime('%Y-%m-%d')   

                #Split the row string into a list of elements
                row = (decoded_bytes)
                row_elements = row.split(",")
                batch_number = 195251
                device_number = 729864
                sql = "INSERT INTO sensor_data (batch_number,device_number,date,time,x_coordinate,y_coordinate,temperature,humidity,light_percentage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                data = (int(batch_number),int(device_number),current_date,current_time,float(row_elements[0]),float(row_elements[1]),float(row_elements[2]), float(row_elements[3]), float(row_elements[4]))
                cursor.execute(sql,data)

                # Commit the changes to the database
                connection.commit()
                
                # Check if the current time has exceeded the start time + duration
                if self.send_to_cloud():
                    cloud.sender() # Send the data to the cloud
                    print("Done uploading to cloud")
                    if self.make_csv():
                        cloud.csv_generator()
                
        except Error as e:
                print(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()
            if port.isOpen() == True:
                port.close()

    def sender(self) -> None:
        '''
        Calls push data functions to upload local batch to the cloud.
        '''
        startID = 0
        endID = 0
        # Since the local database is constantly changing we should determine a range to push and upload that, since pushing 'all' could cause problems
        # Get the ID range to push the sensor data
        if self.managerType != 'local':
            print('Create local manager to modify local database.')  
        else:
            try:  
                connection = mysql.connector.connect(**self.db_config)
                cursor = connection.cursor()
                checkid_query = "SELECT MIN(id) AS startID, MAX(id) AS endID FROM sensor_data"
                cursor.execute(checkid_query)
                result = cursor.fetchone()
                startID = result[0]
                endID = result[1]
                local.pushSensorData(startID,endID)
            except Error as e:
                    print(f"Error: {e}")
            finally:
                if connection.is_connected():
                    local.removeSensorData(startID,endID)
                    reset_query = f"ALTER TABLE sensor_data AUTO_INCREMENT = 1;"
                    cursor.execute(reset_query)
                    print("Done")
                    connection.close()
                    connection.close() 
            
            
    #################### END-> Main functionality of manager ####################



# To run uncomment:
# local = MySQLmanager('local') 
# cloud = MySQLmanager('cloud')
# local.receiver()