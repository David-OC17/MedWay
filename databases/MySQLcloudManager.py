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
from allQuerryResult import QuerryResult

from config import cloud_host, cloud_user, cloud_password, cloud_database, local_host, local_user, local_password, local_database
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
        '''
        if(managerType == 'cloud' or managerType == 'aws'):
            self.managerType = managerType
            db_config = {
                'host': cloud_host,
                'user': cloud_user,
                'password': cloud_password,
                'database': cloud_database
            }
        elif (managerType == 'local'):
            self.managerType = managerType
            db_config = {
                'host': local_host,
                'user': local_user,
                'password': local_password,
                'database': local_database
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
        self.create_batch_position_table()
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
            create_batch_alerts_query = """
            CREATE TABLE IF NOT EXISTS batch_alerts (
                alert_number INT AUTO_INCREMENT PRIMARY KEY,
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

    def create_batch_position_table(self) -> None:
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            create_batch_position_query = """
            CREATE TABLE IF NOT EXISTS batch_position (
                batch_number INT,
                date DATE,
                time TIME,
                x_coordinate FLOAT,
                y_coordinate FLOAT
            );
            """
            cursor.execute(create_batch_position_query)
            connection.commit()
            print("Batch Position table created successfully.")
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
            
            ALTER TABLE batch_position
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

    def pushSensorData(self, starID: int, endID: int) -> bool:
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
            INSERT INTO sensor_data (batch_number, device_number, date, temperature, humidity, light_percentage)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            
            # Execute the query with data_list as a list of tuples
            data_list = self.fetch_data_from_database(starID, endID)
            cursor.executemany(insert_query, data_list)
            
            connection.commit()
            print("Records inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            return True
    
    def pushBatchAlerts(self, startAlertNum: int, endAlertNum: int)-> bool:
        '''
        Takes data from local batch alerts data table from startID to endID and pushes it to the cloud.
        Returns if upload was successful.
        '''
        pass
    
    def pushBatchPosition(self, startDate:date, endDate:date)-> bool:
        '''
        Takes data from local batch position data table from startID to endID and pushes it to the cloud.
        Returns if upload was successful.
        '''
        pass
    
    #################### END -> Push to cloud ####################
    
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





############################################

