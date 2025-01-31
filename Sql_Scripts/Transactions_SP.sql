Create or replace procedure Transactions_sp
AS
BEGIN
MERGE Sales.dbo.Transactions AS target
using Sales.dbo.STG_Transactions AS source
on 