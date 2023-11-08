'''
Test the connection to your local and RDS (remote-cloud) database via this script.
'''
import sys
sys.path.append("../../")

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from databases.config import *

def main():
    local_connection: MySQLConnection = connect(
        host = cloud_host,
        user = cloud_user,
        password = cloud_password,
        database = cloud_database
    )

    cloud_connection: MySQLConnection = connect(
        host = cloud_host,
        user = cloud_user,
        password = cloud_password,
        database = cloud_database
    )

    local_cursor: MySQLCursor = local_connection.cursor()
    print("Connected to local database!")

    local_cursor.close()
    local_connection.close()

    cloud_cursor: MySQLCursor = cloud_connection.cursor()
    print("Connected to RDS!")

    cloud_cursor.close()
    cloud_connection.close()

if __name__ == '__main__':
    main()