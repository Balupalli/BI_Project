## test case for demo
import pytest
import sys
import os
import pandas as pd

# Define a marker in test module so that all tests in the module are run togther
pytestmark = pytest.mark.test_module1_total

@pytest.mark.test_connection
def test_connection(establish_connection):
    sql="select * from stg_transactions"
    establish_connection.execute(sql)
    # Fetch all results
    results = establish_connection.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    #print(df.head())
    assert results is not None

def test_stg_transactions_count(establish_connection):
    sql = "select count(*) from stg_transactions"
    establish_connection.execute(sql)
    # Fetch all results
    results = establish_connection.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==1472952


