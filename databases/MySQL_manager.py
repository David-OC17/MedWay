'''
Here we provide a class to interact witht the MySQL database set up on AWS RDS.
The class has the functionality necesarry to:
* Create the tables in the database ('sensor data', 'batch alerts' and 'batch position' tables)
* Push new incoming data (raw) to 'sensor data' table
* Push to 'batch alerts' based on simple conditions of the raw data
* Push raw data to 'batch position'
* Query all three tables
'''

import mysql.connector
from mysql.connector import Error

from config import host, user, password, database
'''
Store db_config variables in the following format in order to connect to AWS

host = '...'
user = '...'
password = '...'
database = '...'
'''

class MySQL_manager:
    def __init__(self) -> None:
        # Information to connect to AWS database
        db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
    #################### START -> Create tables and stablish relationship ####################
    
    # Run once, to create the tables in the database
    def create_tables(self) -> None:
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
    
    
    # Push raw data to 'sensor data'
    def pushSensorData(self, data):
        pass
    
    def pushBatchAlerts(self, data):
        pass
    
    def pushBatchPosition(self, data):
        pass
    
    def pushSensorData(self, data):
        pass
