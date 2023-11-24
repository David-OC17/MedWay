'''
Test your local configuration of MySQL by creating a test_db and running this script.
'''

import sys
sys.path.append("../../")

from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
# Try the database managers
from databases.MySQLmanager import *


def main():
    # As a prerequisite, create 'test_db' in your local MySQL configuration
    
    # Create a test database manager
    manager = MySQLmanager('local_test')

    # Create a test database
    manager.create_tables()

    # Add data to the tables by simulating
    manager.parseAdd_TEST()

    # Query the database

    # Delete something from the database
    
    # Clear the database for the next test
    #manager.clearDatabase('DELETE ME')
    
if __name__ == '__main__':
    main()