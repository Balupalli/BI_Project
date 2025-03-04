import pytest
import mysql.connector
import json
import os

def getdb_credentials():
    file_name = "config.json"
    project_dir = os.path.dirname(os.path.abspath("config.json"))
    file_path = os.path.join(project_dir,"BI_project_QA","config.json")
    print({file_path})
    print({project_dir})
    # with open automatically closes file out of scope
    with open(file_path,'r') as file:
        data=json.load(file)
    return data
#fixture to connect MYSQL DB
@pytest.fixture(scope="session")
def establish_connection():
    db_credentials = getdb_credentials()
    #print(db_credentials)
    conn = mysql.connector.connect(**db_credentials['DB_CREDENTIALS'])
    cursor=conn.cursor()
    print('Connection established successfully')
    yield cursor
    print('closing db connection')
    cursor.close()
    conn.close()