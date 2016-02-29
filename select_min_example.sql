select CONCAT(people.first_name, ' ', people.second_name) AS full_name, min(amount) AS minimum 
              from mydb.orders 
              join mydb.people
              ON
              people.id = orders.person_id 
              where person_id=5;