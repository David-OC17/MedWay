'''
Here we provide a class to interact without the MySQL database set up on AWS RDS.
The class has the functionality necessary to:
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

from dotenv import load_dotenv
from mysql.connector import Error
from datetime import datetime, timedelta
from mysql.connector import connect
from time import time
import serial
import csv
import os

load_dotenv()

class MySQLmanager:

    def __init__(self, managerType: str) -> None:
        '''
        managerType: 'cloud' = 'aws' or 'local'
            or 'local_test' for testing
        '''

        if (managerType == 'cloud' or managerType == 'aws'):
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
        
        elif (managerType == 'testing'):
            self.managerType = managerType
            self.db_config = {
                'host': os.getenv("CLOUD_HOST_TEST"),
                'user': os.getenv("CLOUD_USER_TEST"),
                'password': os.getenv("CLOUD_PASSWORD_TEST"),
                'database': os.getenv("CLOUD_DATABASE_TEST")
            }

        else:
            raise ValueError("No suitable manager type for constructor of MySQLmanager. Use 'cloud' or 'local'.")
        
        #Get the times for the send and csv generator timing
        self.__cloud_time_flag = time()
        self.__csv_time_flag = time()
        self.create_sensor_data_table()


    def send_to_cloud(self):
        # Set the time duration to 30 minutes (in seconds)
        duration = 30 * 60

        # Check if the current time has exceeded the start time + duration
        if time() - self.__cloud_time_flag > duration:
            self.__cloud_time_flag = time()
            return True
        
        return False


    def make_csv(self):
        # Set the time duration to 24 hours (in hours)
        duration = 60 * 60 * 24

        # Check if the current time has exceeded the start time + duration
        if time() - self.__csv_time_flag > duration:
            self.__csv_time_flag = time()
            return True
        
        return False


    def create_sensor_data_table(self) -> None:
        try:
            connection = connect(**self.db_config)
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


    def fetch_data_from_database(self, start_id:int , end_id:int) -> list:
        '''
        Get a range of rows of values from the local database. Query the range given by startID-endID.
        Returns a list of values.
        '''
        if self.managerType != 'local':
                raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
            
        try:
            connection = connect(**self.db_config)
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


    def pushSensorData(self, starID: int, endID: int) -> None:
        '''
        Takes data from local sensor data table from startID to endID and pushes it to the cloud.
        Returns if upload was successful.
        '''

        # Push all lines into the remote table
        if self.managerType != 'cloud':
            raise ValueError('Only cloud manager can interact with RDS cloud. Create a cloud manager to access.')

        try:
            connection = connect(**self.db_config)
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


    def removeSensorData(self, startID: int, endID: int) -> None:
        '''
        Remove the sensor data in the range given by startID-endID.
        Use it to clean local database and avoid data cloning local-cloud.
        Return if the removal was successful.
        '''
        if self.managerType != 'local':
            raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
        
        try:
            connection = connect(**self.db_config)
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


    def clearDatabase(self, confirmation: str = '') -> None:
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
        
        # confirmation = input('This a destructive action. To confirm, enter Y/y and enter. Any other characters cancel the operation.')
        # if confirmation != 'Y' or confirmation != 'n':
        #     print('Database clearance cancelled.')
        
        # Proceed with clearing the database
        connection = connect(**self.db_config)
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

        except Error as err:
            print(f"Error: {err}")
        finally:
            # Close the cursor and connection
            cursor.close()
            connection.close()
        
    #################### END -> Delete from local ####################
    
    def populateTestDatabase(self) -> None:
        # Check if it's a cloud manager
        if self.managerType != 'testing':
            raise ValueError('Only cloud-testing manager can populate the test RDS cloud. Create a testing manager to access.')

        try:
            connection = connect(**self.db_config)
            cursor = connection.cursor()

            # ID,batch_number,device_number,date,time,x_coordinate,y_coordinate,temperature,humidity,light_percentage
            insert_query = """
            INSERT INTO sensor_data (batch_number, device_number, date, time, x_coordinate, y_coordinate, temperature, humidity, light_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            # Read CSV file and populate data_list
            data_list = []
            with open('../test/data/sensor_data.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip header row
                for row in csvreader:
                    # Remove the ID
                    row = row[1:]
                    data_list.append(tuple(row))

            # Execute the query with data_list as a list of tuples
            cursor.executemany(insert_query, data_list)

            connection.commit()
            print("Records inserted successfully.")

        except Error as e:
            print(f"Error: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    
    #################### START -> CSV Generator ####################

    def csv_generator(self) -> None:
        try:
            print("Generating CSV file...")
            header = ['ID','batch_number','device_number','date','time','x_coordinate','y_coordinate','temperature','humidity','light_percentage']
            
            # Get the previous date
            current_date = datetime.today()
            previous_Date = current_date - timedelta(days=1)   
            
            # Connect to the MySQL database
            connection = connect(**self.db_config)
            cursor = connection.cursor()

            # Open the CSV file in write mode
            with open('./temp/tempData.csv', 'w', newline='') as tempData:
                print("Writing to the file.")
                csv_writer = csv.writer(tempData)
                csv_writer.writerow(header)

                # Convert startDate and endDate to MySQL type for query
                startDate = previous_Date
                mysql_startDate = startDate.strftime("%Y-%m-%d")

                endDate = current_date
                mysql_endDate = endDate.strftime("%Y-%m-%d")

                # Define and execute the SELECT query
                select_query = f"SELECT * FROM sensor_data;"
                cursor.execute(select_query)
                
                # Fetch all rows from the query result
                rows = cursor.fetchall()

                # Write the rows to the CSV file
                for row in rows:
                    csv_writer.writerow(row)

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
            connection = connect(**self.db_config)
            cursor = connection.cursor()
            print("Connected to local database")

            #Open a serial port that is connected to an Arduino
            #Program will wait until all serial data is received from Arduino
            #Port description will vary according to operating system. Linux will be in the form /dev/ttyXXXX and Windows and MAC will be COM#.
            
            port = serial.Serial(port = 'COM3', baudrate = 9600)
            if port.isOpen() == False:
                port.open()

            #Write out a single character encoded in utf-8; this is default encoding for Arduino serial COM
            #This character tells the Arduino to start sending data
            port.write(bytes('x','utf-8'))

            while True:
                #Read in data from Serial until (new line) received
                port_bytes = port.readline()
            
                #Convert received bytes to text format and take out the new line characters and spaces 
                decoded_bytes = (port_bytes[0:len(port_bytes)-2].decode("utf-8").strip('\r\n\n'))
                
                #Retrieve current time and date
                current_time = datetime.now().strftime('%H:%M:%S')
                current_date = datetime.now().strftime('%Y-%m-%d')

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
                connection = connect(**self.db_config)
                cursor = connection.cursor()
                check_id_query = "SELECT MIN(id) AS startID, MAX(id) AS endID FROM sensor_data"
                cursor.execute(check_id_query)
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

if __name__== '__main__':
    # To run uncomment:
    local = MySQLmanager('local') 
    cloud = MySQLmanager('cloud')
    local.receiver()