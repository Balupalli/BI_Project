import pytest
import mysql.connector
import json
import os

def getdb_credentials():
    file_name = "config1.json"
    file_path = os.path.abspath(file_name)
    print({file_path})
    with open(file_path,'r') as file:
        data=json.load(file)
    return data

db_credentials= getdb_credentials()
print(db_credentials['DB_CREDENTIALS'])

