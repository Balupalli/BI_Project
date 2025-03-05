--1. Create Customers table from transactions data
CREATE TABLE Mysql_DB_1.customers(
Customer_Id VARCHAR(100) primary key,
Customer_Age INT,
Customer_Location VARCHAR(100),
Customer_Address VARCHAR(100),
Insert_Timestamp DATETIME,
Update_Timestamp DATETIME);

--2.DROP PROCEDURE IF EXISTS
DROP PROCEDURE IF EXISTS Mysql_DB_1.STG_TRANSACTIONS_TO_CUSTOMERS_DATA;

--3.Set the delimiter to $$ to avoid conflicts with semicolons inside the procedure
DELIMITER $$

--4.CREATE PROCEDURE
CREATE PROCEDURE Mysql_DB_1.STG_TRANSACTIONS_TO_CUSTOMERS_DATA()
BEGIN
    DECLARE max_update_time DATETIME DEFAULT '1900-01-01 00:00:00';

    -- Get the latest updated_at timestamp from Customers table
    SELECT COALESCE(MAX(INSERT_TIMESTAMP), '1900-01-01 00:00:00')
    INTO max_update_time FROM customers;

    -- Insert new records or update existing ones (except `INSERT_TIMESTAMP`)
    INSERT INTO customers (Customer_Id, Customer_Age, Customer_Location, Customer_Address, Insert_Timestamp, Update_Timestamp)
    SELECT DISTINCT
        stg.Customer_Id,
        stg.Customer_Age,
        stg.Customer_Location,
        stg.Billing_Address,
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    FROM STG_TRANSACTIONS stg  -- Correct alias placement
    WHERE stg.INSERT_TIMESTAMP > max_update_time

    ON DUPLICATE KEY UPDATE
        Customer_Age = stg.Customer_Age,
        Customer_Location = stg.Customer_Location,
        Customer_Address = stg.Billing_Address,
        Update_Timestamp = CURRENT_TIMESTAMP;
END $$
--5. roll back delimiter to ;
DELIMITER ;

--6.CALLING THE STORE PROC TO LOAD THE DATA
call Mysql_DB_1.STG_TRANSACTIONS_TO_CUSTOMERS_DATA();