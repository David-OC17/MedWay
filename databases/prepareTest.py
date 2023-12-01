# Use the manager file present in the analysis directory

from MySQLmanager import MySQLmanager

def createTable() -> None:
    manager = MySQLmanager(managerType="testing")
    manager.create_sensor_data_table()
    print("Created tables")
    # manager.csv_generator()

def populateRDS() -> None:
    manager = MySQLmanager(managerType="testing")
    manager.populateTestDatabase()
    print("Populated RDS database.")
    
def populateLocal() -> None:
    manager = MySQLmanager(managerType="local")
    manager.populateTestDatabase()
    print("Populated local database.")

def clearDatabase() -> None:
    manager = MySQLmanager(managerType="testing")
    manager.clearDatabase(confirmation='DELETE ME')
    print("Cleared all the table for sensor data.")

def main() -> None:
    #createTable()
    # populateRDS()
    populateLocal()
    # clearDatabase()
    

if __name__ == "__main__":
    main()