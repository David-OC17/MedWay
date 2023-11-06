'''
Connect and disconnect to the cloud, nothing else.
'''

from config import *
import mysql.connector
from mysql.connector import Error


db_config = {
                'host': cloud_host,
                'user': cloud_user,
                'password': cloud_password,
                'database': cloud_database
            }

# Establish the connection
connection = mysql.connector.connect(**db_config)

# Create a cursor
cursor = connection.cursor()

# Close the connection
connection.close()