--Create a Database
Create Database SAI

--verify if the databse has been created
SELECT name, database_id, create_date  
FROM sys.databases;  
GO
--create a master STG table Transactions to load the data initially
create table SAI.dbo.stg_transactions (
Transaction_Id VARCHAR (100),
Customer_Id VARCHAR(100),
Transaction_Amount VARCHAR (100),
Transaction_Date VARCHAR (100),
Payment_Method VARCHAR(100),
Product_Category VARCHAR(100),
Quantity VARCHAR (100),
Customer_Age VARCHAR (100),
Customer_Location VARCHAR(100),
Device_Used VARCHAR(100),
IP_Address VARCHAR(100),
Shipping_Address VARCHAR(300),
Billing_Address VARCHAR(300),
Is_Fraudulent VARCHAR (100),
Account_Age_Days VARCHAR (100),
Transaction_Hour VARCHAR (100));

--Alter stg table to add column of insert time stamp
Alter table SAI.dbo.stg_transactions 
ADD Insert_Timestamp DATETIME;

--verify the stg table creation
select * from SAI.dbo.stg_transactions;

--create a master table Transactions to load the data 
create table SAI.dbo.transactions (
Transaction_Id VARCHAR (100) Primary key,
Customer_Id VARCHAR(100),
Transaction_Amount Numeric(10,2),
Transaction_Date DATETIME,
Payment_Method VARCHAR(100),
Product_Category VARCHAR(100),
Quantity INT,
Customer_Age INT,
Customer_Location VARCHAR(100),
Device_Used VARCHAR(100),
IP_Address VARCHAR(100),
Shipping_Address VARCHAR(300),
Billing_Address VARCHAR(300),
Is_Fraudulent BIT,
Account_Age_Days NUMERIC(10,0),
Transaction_Hour INT,
Stg_Insert_Timestamp DATETIME,
Insert_Timestamp DATETIME,
Update_Timestamp DATETIME
)