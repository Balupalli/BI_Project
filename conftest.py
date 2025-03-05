import pytest
import mysql.connector
import json
import os

# Add a custom command line option to determine the environment to run automation tests
def pytest_addoption(parser):
    parser.addoption("--env", default="QA", help="Select environment: DEV, QA, or PROD")