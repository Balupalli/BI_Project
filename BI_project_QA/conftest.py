import pytest
import mysql.connector
import json
import os
from sqlalchemy import create_engine

# Add a custom command line option to determine the environment to run automation tests
#def pytest_addoption(parser):
#   parser.addoption("--env", default="QA", help="Select environment: DEV, QA, or PROD")

@pytest.fixture(scope="session")
def test_env(pytestconfig):
    env=pytestconfig.getoption("env")
    db_credentials = getdb_credentials()
    if env=='DEV':
        return db_credentials['DB_CREDENTIALS_DEV']
    elif env=='QA':
        return db_credentials['DB_CREDENTIALS_QA']
    elif env=='PROD':
        return db_credentials['DB_CREDENTIALS_PROD']


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
def establish_connection(test_env):
    #print(db_credentials)
    conn = mysql.connector.connect(**test_env)
    cursor=conn.cursor()
    print('Connection established successfully')
    yield cursor
    print('closing db connection')
    cursor.close()
    conn.close()