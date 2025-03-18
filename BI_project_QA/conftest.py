import pytest
import mysql.connector
import json
import os
from sqlalchemy import create_engine
import pymysql
import logging

# DEFINING A FIXTURE TO CREATE AND CONFIGURE logger. This runs prior to all tests
@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configures logging at the start of the test session."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Creates 'logs' if it doesn't exist
    log_file = os.path.join(log_dir, "test_execution.log")

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set logging level

    # Remove existing handlers if any (prevents duplicate logs)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create a file handler
    file_handler = logging.FileHandler(log_file, mode="w")  # 'w' to overwrite logs on each run
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))

    # Add handler to logger
    logger.addHandler(file_handler)
    logging.info("Starting new pytest session...")

# Add a custom command line option to determine the environment to run automation tests
# def pytest_addoption(parser):
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

#function to retrive the credentials
def getdb_credentials():
    file_name = "config.json"
    project_dir = os.path.dirname(os.path.abspath("config.json"))
    file_path = os.path.join(project_dir,"BI_project_QA","config.json")
    #print({file_path})
    #print({project_dir})
    # with open automatically closes file out of scope
    with open(file_path,'r') as file:
        data=json.load(file)
    return data

#fixture to connect MYSQL DB using cursor but it has performance issues with large data
@pytest.fixture(scope="session")
def establish_connection(test_env):
    #print(db_credentials)
    conn = mysql.connector.connect(**test_env)
    cursor=conn.cursor()
    print('\n Connection established successfully')
    yield cursor
    print('\n closing db connection')
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
    print('\n Connection established successfully')
    yield connection
    print('\n closing db connection')
    connection.close()
    engine.dispose()

