SELECT CONCAT(people.first_name, ' ', people.second_name, ' spent a total of ', SUM(orders.amount)) AS Full_Name,
              SUM(orders.amount) AS Average FROM mydb.people
        JOIN mydb.orders
        ON
        people.id = orders.person_id where person_id=2;
SELECT DISTINCT person_id FROM mydb.orders