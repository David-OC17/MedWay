import mysql.connector
from config import *

def create_connection():
    connection = mysql.connector.connect(
        host = cloud_host,
        user = cloud_user,
        password = cloud_password,
        database = cloud_database
    )
    return connection

if __name__ == '__main__':
    connection = create_connection()
    cursor = connection.cursor()
    print('Connected to AWS database in RDS.')
    cursor.close()
    connection.close()