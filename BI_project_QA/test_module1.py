## test case for demo
import pytest
import sys
import os
import pandas as pd

# Define a marker in test module so that all tests in the module are run togther
pytestmark = pytest.mark.stg_transactions

#1. test case to check DB connection established successfully
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

@pytest.mark.test_connection_sqlalchemy
def test_connection_sql_alchemy(establish_connection_sqlalchemy):
    sql="select * from stg_transactions"
    df = pd.read_sql(sql,establish_connection_sqlalchemy)
    #print(df.head())
    assert df is not None

#2. test case to verify the count of records
def test_stg_transactions_count(establish_connection):
    sql = "select count(*) from stg_transactions"
    establish_connection.execute(sql)
    # Fetch all results
    results = establish_connection.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==1472952

#3. test case to check length of transaction_id , customer_id columns is 36 digit
def test_stg_transactions_trans_id_check(establish_connection):
    sql="select distinct length(transaction_id),length(customer_id) from stg_transactions"
    establish_connection.execute(sql)
    results=establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==36 and df.iloc[0,1]==36

#4.test case to check customer age
def test_stg_transactions_customer_age_check(establish_connection):
    sql=""" select count(*) from stg_transactions
            where customer_age < 0 or customer_age > 100"""
    establish_connection.execute(sql)
    results=establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==0

#5. test case to check transaction amount cannot be null
def test_stg_transactions_transact_amount_not_null_check(establish_connection):
    sql="""select count(*) from stg_transactions
            where transaction_amount is null"""
    establish_connection.execute(sql)
    results=establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==0

#6. test case to check if there is any transaction with no quantity in it
def test_stg_transactions_quantity_check(establish_connection):
    sql=""" select count(*) from stg_transactions
            where quantity is null or quantity <= 0; """
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0, 0] == 0

#7. test case to check the transaction hour column is getting right data
def test_stg_transactions_transaction_hour_check(establish_connection):
    sql=""" select count(*) from stg_transactions
            where transaction_hour not between 1 and 24;"""
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0, 0] == 0









