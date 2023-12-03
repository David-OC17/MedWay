from MySQLmanager import MySQLmanager

# Create the original tables in the database
if __name__ == "__main__":
    #Create the local database
    local_manager = MySQLmanager('local')
    local_manager.create_sensor_data_table()
    
    # cloud_manager = MySQLmanager('cloud')
    # cloud_manager.create_sensor_data_table()