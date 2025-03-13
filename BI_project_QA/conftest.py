import pytest
import mysql.connector
import json
import os
from sqlalchemy import create_engine
import pymysql

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

#fixture to connect MYSQL DB using cursor but it is has performance issues with large data
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

#fixture to connect MYSQL DB using sqlalchemy engine it has good performance with large data
@pytest.fixture(scope="session")
def establish_connection_sqlalchemy(test_env):
    user= test_env["user"]
    password=test_env["password"]
    host=test_env["host"]
    database=test_env["database"]
    # Create an SQLAlchemy engine
    # we are using mysqldb driver which is efficient for multi threading and good memory usage
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:3306/{database}")
    # Test the connection
    connection = engine.connect()
    print('Connection established successfully')
    yield connection
    print('closing db connection')
    connection.close()
    engine.dispose()

