# Use the manager file present in the analysis directory

from MySQLmanager import MySQLmanager

def createTable() -> None:
    manager = MySQLmanager(manager_type="testing")
    manager.create_sensor_data_table()
    print("Created tables")
    # manager.csv_generator()

def populateRDS() -> None:
    manager = MySQLmanager(manager_type="testing")
    manager.populate_test_database()
    print("Populated RDS database.")
 
def populateLocal() -> None:
    manager = MySQLmanager(manager_type="local")
    manager.populate_test_database()
    print("Populated local database.")

def clearDatabase() -> None:
    manager = MySQLmanager(manager_type="testing")
    manager.clear_database(confirmation='DELETE ME')
    print("Cleared all the table for sensor data.")

def main() -> None:
    # createTable()
    # populateRDS()
    populateLocal()
    # clearDatabase()

if __name__ == "__main__":
    main()
