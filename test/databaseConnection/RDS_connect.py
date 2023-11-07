
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from config import cloud_host, cloud_user, cloud_password, cloud_database

connection: MySQLConnection = connect(
    host = cloud_host,
    user = cloud_user,
    password = cloud_password,
    database = cloud_database
)

cursor: MySQLCursor = connection.cursor()
print("Connected to RDS!")

cursor.close()
connection.close()