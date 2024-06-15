import os
from google.cloud.sql.connector import Connector
import pymysql
import sqlalchemy
from sqlalchemy import text

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    instance_connection_name = "mlconsole-poc:us-central1:jai-dev-sql"
    db_user = "root"
    db_pass = "jai-dev-2023"
    db_name = "jai-dev-db"

    connector = Connector()

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        print("Connected to cloud sql instance.")
        return conn

    pool = sqlalchemy.create_engine("mysql+pymysql://", creator=getconn)
    return pool

def show_databases():
    engine = connect_with_connector()

    connection = engine.connect()

    result = connection.execute(text("SHOW DATABASES;"))

    for database in result:
        print("Database",database)

    connection.close()

show_databases()