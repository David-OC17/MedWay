'''
This file is a stripped down version of the complete MySQLmanager in the databases directory.
Upload this to AWS Lambda to set up the working system.
'''

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import csv
from datetime import datetime, timedelta

load_dotenv()

class MySQLmanager:            
    def __init__(self, testing:bool=False) -> None:
        '''
        managerType: 'cloud' = 'aws' or 'local'
            or 'local_test' for testing
        '''
        if testing:
            self.db_config = {
                'host': os.getenv("CLOUD_HOST_TEST"),
                'user': os.getenv("CLOUD_USER_TEST"),
                'password': os.getenv("CLOUD_PASSWORD_TEST"),
                'database': os.getenv("CLOUD_DATABASE_TEST")
            }
        else:
            self.db_config = {
                'host': os.getenv("CLOUD_HOST"),
                'user': os.getenv("CLOUD_USER"),
                'password': os.getenv("CLOUD_PASSWORD"),
                'database': os.getenv("CLOUD_DATABASE")
            }

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
            SELECT batch_number,device_number,date,time,x_coordinate,y_coordinate,temperature,humidity,light_percentage
            FROM sensor_data
            WHERE ID BETWEEN %s AND %s
            """
            cursor.execute(select_query, (start_id, end_id))

            data_list = []
            for row in cursor.fetchall():
                # Append each row as a tuple to the data list
                print(row)
                data_list.append(row)

            return data_list # Return the tuple
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def csv_generator(self) -> None:
        try:
            print("Generating CSV file...")
            header = ['ID','batch_number','device_number','date','time','x_coordinate','y_coordinate','temperature','humidity','light_percentage']
            
            # Get the previous date
            current_date = datetime.today()
            previous_Date = current_date - timedelta(days=1)   
            
            # Connect to the MySQL database
            connection = mysql.connector.connect(**self.db_config)
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