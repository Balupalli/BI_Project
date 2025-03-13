import pytest
import mysql.connector
import json
import os
import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

user='root'
password='Usa1234'
host='localhost'
database='Mysql_DB_1'

print(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")
    # Test the connection
connection = engine.connect()
print('Connection established successfully')
sql = "select * from stg_transactions"
df = pd.read_sql(sql, connection)
print(df.columns)
print('Closing DB connection')
connection.close()
engine.dispose()


