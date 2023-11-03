from MedWay.databases.MySQLcloudManager import MySQL_manager

# Create the original tables in the database
if __name__ == "__main__":
    #Create the local database
    local_manager = MySQL_manager('local')
    local_manager.create_tables()
    
    cloud_manager = MySQL_manager('cloud')
    cloud_manager.create_tables()