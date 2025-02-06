 ##1. Install My SQL connector
##pip install pandas mysql-connector-python

 ##2. Install required packages

import pandas as pd
import mysql.connector

# read data from local
df = pd.read_csv('/Users/saiprakashreddybalupalli/PycharmProjects/BI_Project/Fraudulent_E-Commerce_Transaction_Data.csv')

# Establish MySQL connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Usa@1234',
    database='Mysql_DB_1'
)
cursor = conn.cursor()

# Convert DataFrame to List of Tuples
data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]

# SQL Insert Query
sql = """INSERT INTO stg_transactions (
    Transaction_Id, Customer_Id, Transaction_Amount, Transaction_Date, Payment_Method,
    Product_Category, Quantity, Customer_Age, Customer_Location, Device_Used, 
    IP_Address, Shipping_Address, Billing_Address, Is_Fraudulent, Account_Age_Days, 
    Transaction_Hour
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

# Split into batches of 10,000 rows
batch_size = 10000
batches = [data_tuples[i:i + batch_size] for i in range(0, len(data_tuples), batch_size)]

try:
    for batch in batches:
        cursor.executemany(sql, batch)  # Insert batch
        conn.commit()  # Commit after each batch
        print(f"{len(batch)} records inserted successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")
    conn.rollback()

finally:
    cursor.close()
    conn.close()