SELECT * FROM mydb.orders
WHERE created_at
BETWEEN
'2016-02-16 14:48:00'
AND
'2016-02-16 22:34:00'
and not
amount < 12.00;