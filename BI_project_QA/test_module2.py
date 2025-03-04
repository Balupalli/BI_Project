import pytest
import sys
import os
import pandas as pd

pytestmark=pytest.mark.transactions
#1. test case to check the DB connection
@pytest.mark.test_connection
def test_connection(establish_connection):
    sql="select * from transactions"
    establish_connection.execute(sql)
    # Fetch all results
    results = establish_connection.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    #print(df.head())
    assert results is not None

#2. test case to check the duplicates in transactions table
def test_transactions_duplicates(establish_connection):
    sql = """ select count(*) from 
              (select transaction_id, count(*) from transactions
              group by transaction_id
              having count(*)>1) CTE;"""
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==0

#3. test case to check the count of records between stg_transactions & transactions
def test_transactions_stg_transactions_count_check(establish_connection):
    sql=""" select count(*) from stg_transactions
            union all
            select count(*) from transactions;"""
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0] -  df.iloc[1,0] ==0

#4. test case to compare data between stg_transactions and transactions
def test_transactions_stg_transactions_data_check(establish_connection):
    sql=""" select count(*) from (
            select transaction_id, customer_id, transaction_amount, transaction_date, payment_method,
            product_category, quantity, customer_age, customer_location, device_used, ip_address,
            shipping_address, billing_address,is_fraudulent, account_age_days, transaction_hour,
            insert_timestamp from stg_transactions
            minus
            select transaction_id, customer_id, transaction_amount, transaction_date, payment_method,
            product_category, quantity, customer_age, customer_location, device_used, ip_address,
            shipping_address, billing_address,is_fraudulent, account_age_days, transaction_hour,
            stg_insert_timestamp from transactions);"""
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==0
#5. test case to compare data between stg_transactions and transactions
def test_transactions_stg_transactions_data_check2(establish_connection):
    sql=""" select count(*) from stg_transactions s
            left join transactions t on s.transaction_id=t.transaction_id
            where t.transaction_id is null;"""
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==0

#6. test case to compare data between stg_transactions and transactions
def test_transactions_stg_transactions_data_check3(establish_connection):
    sql=""" select count(*) from stg_transactions s
            left join transactions t on s.transaction_id=t.transaction_id
            where t.transaction_id is not null and (t.customer_id <> s.customer_id
            or t.transaction_amount <> s.transaction_amount
            or t.transaction_date <> s.transaction_date
            or t.payment_method <> s.payment_method
            or t.product_category <> s.product_category
            or t.quantity <> s.quantity
            or t.customer_age <> s.customer_age
            or t.customer_location <> s.customer_location
            or t.device_used <> s.device_used
            or t.ip_address <> s.ip_address
            or t.shipping_address <> s.shipping_address
            or t.billing_address <> s.billing_address
            or t.is_fraudulent <> s.is_fraudulent
            or t.account_age_days <> s.account_age_days
            or t.transaction_hour <> s.transaction_hour)"""
    establish_connection.execute(sql)
    results = establish_connection.fetchall()
    df = pd.DataFrame(results, columns=[col[0] for col in establish_connection.description])
    assert df.iloc[0,0]==0