"""
  Database configuration file. The project is connected to the MySQL database.
  The below code describes the database name, user,password of the mysql database.
"""
DEBUG = True
import pymysql
import time
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_DB = 'jai-dev-db'
# MYSQL_HOST = 'localhost'
MYSQL_HOST= 'cloudsql_proxy'
MYSQL_PORT = 3308

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

