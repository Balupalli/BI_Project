--PRE CONDITIONS FOR RUNNING THE STORE PROC
--1. To see if source table has any data
SELECT * FROM STG_TRANSACTIONS;

-- UPDATE TABLE TO POPULATE THE INSERT TIMESTAMP since it is found null
UPDATE STG_TRANSACTIONS 
SET INSERT_TIMESTAMP = CURRENT_TIMESTAMP;

--UNIQUE INDEX CREATION ON TABLE SO THAT STORE PROC USES IT FOR MERGING DATA
CREATE UNIQUE INDEX idx_name ON TRANSACTIONS(TRANSACTION_ID);


--CREATE A STORE PROC TO MOVE DATA FROM STG_TRANSACTIONS TO TRANSACTIONS
--Note: all commands must be run on terminal dbvisualiser doesnt support it
--1.DROP PROCEDURE IF EXISTS
DROP PROCEDURE IF EXISTS Mysql_DB_1.STG_TRANSACTIONS_TO_TRANSACTIONS_DATA;

-- 2.Set the delimiter to $$ to avoid conflicts with semicolons inside the procedure
DELIMITER $$

--3. initialise proc
CREATE PROCEDURE Mysql_DB_1.STG_TRANSACTIONS_TO_TRANSACTIONS_DATA()
BEGIN
    DECLARE max_update_time DATETIME DEFAULT '1900-01-01 00:00:00';

    -- Get the latest updated_at timestamp from TableB
    SELECT COALESCE(MAX(INSERT_TIMESTAMP), '1900-01-01 00:00:00') INTO max_update_time FROM TRANSACTIONS;

    -- Insert new records or update existing ones (except `INSERT_TIMESTAMP`)
    INSERT INTO TRANSACTIONS (TRANSACTION_ID, CUSTOMER_ID, TRANSACTION_AMOUNT, TRANSACTION_DATE, PAYMENT_METHOD, PRODUCT_CATEGORY, QUANTITY,
    CUSTOMER_AGE, CUSTOMER_LOCATION, DEVICE_USED, IP_ADDRESS, SHIPPING_ADDRESS, BILLING_ADDRESS, IS_FRAUDULENT, ACCOUNT_AGE_DAYS, TRANSACTION_HOUR,
    STG_INSERT_TIMESTAMP, INSERT_TIMESTAMP, UPDATE_TIMESTAMP)
    SELECT TRANSACTION_ID, CUSTOMER_ID, TRANSACTION_AMOUNT, TRANSACTION_DATE, PAYMENT_METHOD,
           PRODUCT_CATEGORY, QUANTITY, CUSTOMER_AGE, CUSTOMER_LOCATION, DEVICE_USED, IP_ADDRESS,
           SHIPPING_ADDRESS, BILLING_ADDRESS, IS_FRAUDULENT, ACCOUNT_AGE_DAYS, TRANSACTION_HOUR,
           INSERT_TIMESTAMP, CURRENT_TIMESTAMP AS INSERT_TIMESTAMP, CURRENT_TIMESTAMP AS UPDATE_TIMESTAMP
    FROM STG_TRANSACTIONS
    WHERE INSERT_TIMESTAMP > max_update_time  -- Only fetch new/modified records
    ON DUPLICATE KEY UPDATE 
        TRANSACTION_ID = VALUES(TRANSACTION_ID), 
        CUSTOMER_ID = VALUES(CUSTOMER_ID),
        TRANSACTION_AMOUNT = VALUES(TRANSACTION_AMOUNT),
        TRANSACTION_DATE = VALUES(TRANSACTION_DATE),
        PAYMENT_METHOD = VALUES(PAYMENT_METHOD),
        PRODUCT_CATEGORY = VALUES(PRODUCT_CATEGORY),
        QUANTITY = VALUES(QUANTITY),
        CUSTOMER_AGE = VALUES(CUSTOMER_AGE),
        CUSTOMER_LOCATION = VALUES(CUSTOMER_LOCATION),
        DEVICE_USED = VALUES(DEVICE_USED),
        IP_ADDRESS = VALUES(IP_ADDRESS),
        SHIPPING_ADDRESS = VALUES(SHIPPING_ADDRESS),
        BILLING_ADDRESS = VALUES(BILLING_ADDRESS),
        IS_FRAUDULENT = VALUES(IS_FRAUDULENT),
        ACCOUNT_AGE_DAYS = VALUES(ACCOUNT_AGE_DAYS),
        TRANSACTION_HOUR = VALUES(TRANSACTION_HOUR),
        STG_INSERT_TIMESTAMP = VALUES(INSERT_TIMESTAMP),
        UPDATE_TIMESTAMP = CURRENT_TIMESTAMP; -- Do not update `INSERT_TIMESTAMP`
END $$

--4. roll back delimiter to ;
DELIMITER ;

--5.CALLING THE STORE PROC TO LOAD THE DATA
call Mysql_DB_1.STG_TRANSACTIONS_TO_TRANSACTIONS_DATA();

--6.see the target table has data generated
select * from transactions;