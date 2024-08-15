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

'''
TODO Modify comments for simplicity.
TODO Make main file description clearer.
TODO Make function names consistent.
'''

from dotenv import load_dotenv
from mysql.connector import Error
from datetime import datetime
from mysql.connector import connect
from time import time
import logging
from serial import Serial
import csv
import os
import numpy as np

load_dotenv()
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

class MySQLmanager:

    def __init__(self, managerType: str) -> None:
        """
        Initializes the MySQLmanager instance based on the provided manager type.

        Parameters:
        managerType (str): The type of manager to initialize. 
                        Options are 'cloud', 'aws' for cloud-based management,
                        'local' for local database management, and 'testing' for cloud testing.

        Raises:
        ValueError: If an invalid managerType is provided.
        """


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
        
        self.__cloud_time_flag = time()
        self.__csv_time_flag = time()
        self.create_sensor_data_table()


    def send_to_cloud(self):
        duration = 30 * 60 #seconds
        
        if time() - self.__cloud_time_flag > duration:
            self.__cloud_time_flag = time()
            return True
        
        return False


    def make_csv(self):
        duration = 60 * 60 * 24 #seconds

        if time() - self.__csv_time_flag > duration:
            self.__csv_time_flag = time()
            return True
        
        return False


    def create_sensor_data_table(self) -> None:
        """
        Creates the 'sensor_data' table in the database if it does not already exist.

        This table stores sensor data including batch number, device number, date, time, and various sensor measurements.

        Raises:
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        """

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
            logging.debug('Sensor data table created successfully.')

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def fetch_data_from_database(self, start_id:int , end_id:int) -> list:
        """
        Fetches a range of records from the 'sensor_data' table in the local database.

        Parameters:
        start_id (int): The starting ID of the records to fetch.
        end_id (int): The ending ID of the records to fetch.

        Returns:
        list: A list of tuples, where each tuple contains the data for one record.

        Raises:
        ValueError: If the manager type is not 'local'.
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        """

        if self.managerType != 'local':
                raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
            
        try:
            connection = connect(**self.db_config)
            cursor = connection.cursor()

            select_query = """
            SELECT batch_number,device_number,date,time,x_coordinate,y_coordinate,temperature,humidity,light_percentage
            FROM sensor_data
            WHERE ID BETWEEN %s AND %s
            """
            cursor.execute(select_query, (start_id, end_id))

            data_list = []
            for row in cursor.fetchall():
                data_list.append(row)

            return data_list

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()  


    def pushSensorData(self, starID: int, endID: int) -> None:
        """
        Pushes a range of sensor data from the local database to the cloud database.

        Parameters:
        startID (int): The starting ID of the records to push.
        endID (int): The ending ID of the records to push.

        Raises:
        ValueError: If the manager type is not 'cloud'.
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        """

        if self.managerType != 'cloud':
            raise ValueError('Only cloud manager can interact with RDS cloud. Create a cloud manager to access.')

        try:
            connection = connect(**self.db_config)
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO sensor_data (batch_number,device_number,date,time, x_coordinate,y_coordinate,temperature,humidity,light_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s ,%s ,%s);
            """
            
            # Execute the query with data_list as a list of tuples
            data_list = local.fetch_data_from_database(starID, endID)
            cursor.executemany(insert_query, data_list)
            
            connection.commit()
            logging.debug('Records inserted successfully.')

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def removeSensorData(self, startID: int, endID: int) -> None:
        """
        Removes a range of records from the 'sensor_data' table in the local database.

        This is used to prevent duplicate data after it has been successfully uploaded to the cloud.

        Parameters:
        startID (int): The starting ID of the records to remove.
        endID (int): The ending ID of the records to remove.

        Raises:
        ValueError: If the manager type is not 'local'.
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        """

        if self.managerType != 'local':
            raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')
        
        try:
            connection = connect(**self.db_config)
            cursor = connection.cursor()
            
            delete_query = f"DELETE FROM sensor_data WHERE id >= {startID} AND id <= {endID}"
            
            cursor.execute(delete_query)
            
            connection.commit()
            logging.debug('Range of rows deleted successfully from sensor data.')

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def clearDatabase(self, confirmation: str = '') -> None:
        """
        Clears all tables from the local or test database.

        This method is primarily for testing purposes. It requires a confirmation string to execute.

        Parameters:
        confirmation (str): The confirmation string required to clear the database. Must be 'DELETE ME'.

        Raises:
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        """

        if confirmation != 'DELETE ME':
            logging.warning('Confirmation not received, not clearing the database.')
        elif self.managerType != 'local_test':
            logging.warning('You may only clear all the database during testing and with a local_test manager.')
        
        connection = connect(**self.db_config)
        cursor = connection.cursor()
    
        try:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            for table in tables:
                table_name = table[0]
                drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
                cursor.execute(drop_table_query)
                logging.debug(f"Dropped table: {table_name}")

            connection.commit()

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            cursor.close()
            connection.close()
        
    
    def populateTestDatabase(self) -> None:
        """
        Populates the 'sensor_data' table in the test database with sample data from a CSV file.

        This method is intended for testing purposes to simulate sensor data uploads.

        Raises:
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        FileNotFoundError: If the CSV file with test data cannot be found.
        """

        try:
            connection = connect(**self.db_config)
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO sensor_data (batch_number, device_number, date, time, x_coordinate, y_coordinate, temperature, humidity, light_percentage)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            data_list = []
            with open('../test/data/sensor_data.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)
                for row in csvreader:
                    row = row[1:]  # Ignore the ID
                    data_list.append(tuple(row))

            cursor.executemany(insert_query, data_list)

            connection.commit()
            logging.debug("Records inserted successfully.")

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


    def csv_generator(self) -> None:
        """
        Generates a CSV file containing all records from the 'sensor_data' table.

        This CSV file is saved to a temporary location and can be used for backups or data analysis.

        Raises:
        connect.Error: If there is an error connecting to the database or executing the SQL query.
        """

        try:
            logging.debug('Generating CSV file...')
            header = ['ID','batch_number','device_number','date','time','x_coordinate','y_coordinate','temperature','humidity','light_percentage']
            
            connection = connect(**self.db_config)
            cursor = connection.cursor()

            with open('./temp/tempData.csv', 'w', newline='') as tempData:
                logging.debug('Writing to the file.')
                csv_writer = csv.writer(tempData)
                csv_writer.writerow(header)

                # TODO: Make the selected data a sliding window, avoiding overlap with past 

                select_query = f"SELECT * FROM sensor_data;"
                cursor.execute(select_query)
                
                rows = cursor.fetchall()

                for row in rows:
                    csv_writer.writerow(row)

        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                logging.debug('CSV file generated successfully.')


    def receiver(self) -> None:
        """
        Continuously listens for incoming data streams from sensors and stores the data in the local database.

        The method will periodically attempt to send the data to the cloud and generate a CSV backup.

        Raises:
        ValueError: If the manager type is not 'local'.
        connect.Error: If there is an error connecting to the database.
        serial.SerialException: If there is an error with the serial port communication.
        """

        if self.managerType != 'local':
            raise ValueError('Cloud manager cannot alter local database. Create local manager to modify local database.')

        try:
            connection = connect(**self.db_config)
            cursor = connection.cursor()
            logging.info('Connected to local database.')

            # Port description will vary according to operating system.
            # Linux will be in the form /dev/ttyXXXX and Windows and MAC will be COM#.
            port = Serial(port = '/dev/ttyUSB0', baudrate = 115200)
            if port.isOpen() == False:
                port.open()

            port.write(bytes('x','utf-8')) # Arduino start sending data

            while True:
                port_bytes = port.readline()
            
                decoded_bytes = (port_bytes[0:len(port_bytes)-2].decode("utf-8").strip('\r\n\n'))
                
                current_time = datetime.now().strftime('%H:%M:%S')
                current_date = datetime.now().strftime('%Y-%m-%d')

                row_elements = (decoded_bytes).split(",")
                batch_number = 195251
                device_number = 729864
                sql = "INSERT INTO sensor_data (batch_number,device_number,date,time,x_coordinate,y_coordinate,temperature,humidity,light_percentage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                light_dummy :np.float64 = 15 * np.random.random_sample()
                data = (int(batch_number),int(device_number),current_date,current_time,float(row_elements[0]),float(row_elements[1]),float(row_elements[2]), float(row_elements[3]), light_dummy)
                cursor.execute(sql,data)

                connection.commit()
                
                if self.send_to_cloud():
                    cloud.sender()
                    logging.info("Done uploading to cloud.")
                    if self.make_csv():
                        cloud.csv_generator()
                
        except connect.Error as e:
            logging.error(f"Database Error: {e}")
            raise
        except Serial.SerialException as e:
            logging.error(f"Serial Port Error: {e}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise

        finally:
            if connection.is_connected():
                connection.close()
            if port.isOpen() == True:
                port.close()


    def sender(self) -> None:
        """
        Uploads all sensor data from the local database to the cloud database.

        After uploading, it removes the uploaded data from the local database to prevent duplication.

        Raises:
        connect.Error: If there is an error connecting to the database or executing the SQL queries.
        """

        startID = 0
        endID = 0

        if self.managerType != 'local':
            logging.info('Create local manager to modify local database.')
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

            except connect.Error as e:
                logging.error(f"Database Error: {e}")
                raise
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                raise

            finally:
                if connection.is_connected():
                    local.removeSensorData(startID,endID)
                    reset_query = f"ALTER TABLE sensor_data AUTO_INCREMENT = 1;"
                    cursor.execute(reset_query)
                    connection.close()
                    connection.close() 
                    logging.info('Done')
            

if __name__== '__main__':
    local = MySQLmanager('local') 
    cloud = MySQLmanager('cloud')
    local.receiver()