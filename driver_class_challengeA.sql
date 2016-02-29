
/*select avg(amount) from mydb.orders where person_id=2;*/
/*SELECT concat(first_name, ' ', second_name) AS full_name FROM `mydb`.`people`;*/
/*SELECT CONCAT(people.first_name, ' ', people.second_name) AS fullname, SUM(orders.amount) AS total_spend
      FROM `mydb`.`people`
      JOIN `mydb`.`orders`
      ON people.id = orders.person_id
      GROUP BY people.id;*/
SELECT CONCAT(people.first_name, ' spends') AS First_Name, AVG(amount) AS Average FROM mydb.people
        JOIN mydb.orders
        ON
        people.id = orders.person_id where person_id=1;