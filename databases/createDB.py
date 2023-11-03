from MySQL_manager import MySQL_manager

# Create the original tables in the database
if __name__ == "__main__":
    manager = MySQL_manager()
    manager.create_tables()
