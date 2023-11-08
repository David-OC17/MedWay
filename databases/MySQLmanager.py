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
from datetime import date
from .allQuerryResult import QuerryResult

from .config import *
'''
Store db_config variables in the following format in order to connect to AWS

host = '...'
user = '...'
password = '...'
database = '...'
'''

class MySQLmanager:
    def __init__(self, managerType: str) -> None:
        '''
        managerType: 'cloud' = 'aws' or 'local'
            or 'local_test' for testing
        '''
        if(managerType == 'cloud' or managerType == 'aws'):
            self.managerType = managerType
            self.db_config = {
                'host': cloud_host,
                'user': cloud_user,
                'password': cloud_password,
                'database': cloud_database
            }
        elif (managerType == 'local'):
            self.managerType = managerType
            self.db_config = {
                'host': local_host,
                'user': local_user,
                'password': local_password,
                'database': local_database
            }
        elif (managerType == 'local_test'):
            self.managerType = managerType
            self.db_config = {
                'host': test_host,
                'user': test_user,
                'password': test_password,
                'database': test_database
            }
        else:
            raise ValueError("No suitable manager type for constructor of MySQLmanager. Use 'cloud' or 'local'.")
        
    #################### START -> Create tables and stablish relationship ####################

    def create_tables(self) -> None:
        '''
        Run once, to create the tables in the database
        '''
        self.create_sensor_data_table()
        self.create_batch_alerts_table()
        self.establish_relationships()
        
    def create_sensor_data_table(self) -> None:
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            create_sensor_data_query = """
            CREATE TABLE IF NOT EXISTS sensor_data (
                ID INT AUTO_INCREMENT PRIMARY KEY,
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

    def create_batch_alerts_table(self) -> None:
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            # The ID key is used in both tables, but only full IDs will be present in sensor_data table,
            #   since not all of them generate an alert for batch_alerts table
            create_batch_alerts_query = """
            CREATE TABLE IF NOT EXISTS batch_alerts (
                ID INT PRIMARY KEY,
                alert_number AUTO_INCREMENT INT ,
                batch_number INT,
                temperature_alert BOOLEAN,
                humidity_alert BOOLEAN,
                light_alert BOOLEAN
            );
            """
            cursor.execute(create_batch_alerts_query)
            connection.commit()
            print("Batch Alerts table created successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                
    # Establish relationships between tables using foreign keys (batch number)
    def establish_relationships(self) -> None:
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            foreign_key_query = """
            ALTER TABLE batch_alerts
            ADD FOREIGN KEY (batch_number) REFERENCES sensor_data(batch_number);
            """
            cursor.execute(foreign_key_query)
            connection.commit()
            print("Relationships established successfully.")
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
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()

            # Query to fetch data within the specified ID range
            select_query = """
            SELECT column1, column2, column3, ...
            FROM your_table_name
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
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Define the INSERT INTO query with placeholders for data
            insert_query = """
            INSERT INTO sensor_data (batch_number, device_number, date, time, x_coordinate, y_coordinate temperature, humidity, light_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s ,%s ,%s);
            """
            
            # Execute the query with data_list as a list of tuples
            data_list = self.fetch_data_from_database(starID, endID)
            cursor.executemany(insert_query, data_list)
            
            connection.commit()
            print("Records inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def pushBatchAlerts(self, startAlertNum: int, endAlertNum: int)-> None:
        '''
        Takes data from local batch alerts data table from startID to endID and pushes it to the cloud.
        Returns if upload was successful.
        '''
        pass
    
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
            raise ValueError('CLoud manager cannot alter local database. Create local manager to modify local database.')
        
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
        
    def removeBatchAlerts(self, startID: int, endID: int)-> None:
        '''
        Remove the sensor data in the range given by startAlertNum-endAlertNum.
        Use it to clean local database and avoid data cloning local-cloud.
        Return if the removal was successfull.
        '''
        if self.managerType != 'local':
            raise ValueError('CLoud manager cannot alter local database. Create local manager to modify local database.')
        
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            delete_query = f"DELETE FROM batch_alerts WHERE id >= {startID} AND id <= {endID}"
            
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
    
    #################### START -> Querry tables ####################
    '''
    Provides the ability to query all tables all at once for a given date range or batch number.
    '''
    
    def querryAllByDate(self, startDate:date, endDate:date):
        '''
        Querry cloud database for all the data corresponding to the given dates.
        Return a class QuerryResult with numpy arrays with the information.
        '''
        pass
    
    #################### END -> Querry tables ####################
    
    #################### START -> Parse and add to local ####################
    
    def parseAdd_TEST(self) -> None:
        '''
        TEST METHOD, DO NOT USE DURING PRODUCTION
        Receives a string of data, which is the incoming serial flow from the sensoring module.
        Parse the data and add it to the corresponding local database and tables.
        '''
        
        if self.managerType != 'local_test':
            raise ValueError('Local or cloud managers cannot alter test database. Create test manager to modify test_db.')
        
        # PARSING LOGIC MISSING, ADDING FROM TEST DATA FILE
        # Read from /test_data.csv using Pandas
        import pandas as pd
        from mysql.connector import connect
        from mysql.connector.connection import MySQLConnection
        from mysql.connector.cursor import MySQLCursor
        from databases.config import test_host, test_user, test_password, test_database
        
        df = pd.read_csv('../data/test_data.csv')

        # Extract data for temperature, humidity, and light
        temperature = df['temperature']
        humidity = df['humidity']
        light = df['light_percentage']
        
        # Establish connection to test_db
        local_connection: MySQLConnection = connect(
            host = test_host,
            user = test_user,
            password = test_password,
            database = test_database
        )
        
        local_cursor: MySQLCursor = local_connection.cursor()
        print("Connected to test database!")
        
        # Recursively add data to test_db, simulating data entering from the incoming serial data
        for row in df:
            # Make a query
            print()
            
        local_cursor.close()
        local_connection.close()        
    
    def parseAdd(self, data:str) -> None:
        '''
        Receives a string of data, which is the incoming serial flow from the sensoring module.
        Parse the data and add it to the corresponding local database and tables.
        '''
        
        # PARSING LOGIC MISSING
        pass
    
    #################### END -> Parse and add to local ####################
    
    #################### START -> Main functionality of manager ####################
    
    def receiver(self) -> None:
        '''
        Run when using 'local' manager in order to listen for incoming data streams to be stored in local database (later to be pushed to cloud)
        '''
        if self.managerType != 'local':
            raise ValueError('CLoud manager cannot alter local database. Create local manager to modify local database.')
        # Receive incoming data stream
        # Parse data stream
        # Check for data alerts to be sent to corresponding database
        # Send to local database
        
    def sender(self) -> bool:
        '''
        Calls push data functions to upload local batch to the cloud.
        Returns if uploads were successful.
        '''
        # Since the local database is constantly changing we should determine a range to push and upload that, since pushing 'all' could cause problems
        # Get the ID range to push the sensor data
        
        # Get the alert number range to push the alert data
        
        # Get the the date and time range for the position data alert
        pass

    #################### END-> Main functionality of manager ####################