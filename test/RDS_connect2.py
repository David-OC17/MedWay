import pymysql
from ..databases.config import cloud_host, cloud_user, cloud_password, cloud_database, cloud_port


connection = pymysql.connect(host=cloud_host, user=cloud_user, password=cloud_password, port=cloud_port)
pymysql.connect(cloud_host, cloud_user, cloud_password, cloud_database)

cursor = connection.cursor()

print('Connected to RDS database!')

connection.close()