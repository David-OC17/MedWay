
from mysql.connector import MySQLConnection, connect
from mysql.connector.cursor import MySQLCursor
from os import getenv


class LocalDBConnection:
    """
    Contains the methods for connecting to the local database.

    The database access credentials should be provided in the .env file.
    """

    def __init__(self) -> None:
        # Private attributes
        # self.__database: MySQLConnection = connect(
        #     host = getenv("LOCAL_DB_HOST"),
        #     user = getenv("LOCAL_DB_USER"),
        #     password = getenv("LOCAL_DB_PASSWORD"),
        #     database = getenv("LOCAL_DB_DATABASE")
        # )
        self.__database: MySQLConnection = connect(
            host = "test-cloud-database.ctqvdwxx2rl5.us-east-2.rds.amazonaws.com",
            user = "admin",
            password = "YaelUwU1234",
            database = "test_cloud_database"
        )
        self.__cursor: MySQLCursor = self.__database.cursor()


    def get_last_data_batch(self) -> list[tuple[str]]:
        """
        Gets the last data batch from the local database. Ideally, this method should
        return the last 30 entries from the local database.

        Parameters:
            - Doesn't take any parameters.

        Returns:
            - :return:`data` (list[tuple[str]]): The last batch of data from the local database.
        """

        self.__cursor.execute("SELECT * FROM sensor_data")

        return self.__cursor.fetchall()
