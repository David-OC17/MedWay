'''
Connect and disconnect to the cloud, nothing else.
'''

import mysql.connector
from mysql.connector import Error
from ..databases.config import cloud_host, cloud_user, cloud_password, cloud_database, cloud_port

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