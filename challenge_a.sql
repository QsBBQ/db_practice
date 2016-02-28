USE mydb;
  CREATE table people (
            	    id INTEGER auto_increment,
                    first_name varchar(50) not null,
                    second_name varchar(50) not null,
                    DOB date not null,
                    primary key (id)
            );
  CREATE INDEX people_index_firstname ON people (first_name);
  CREATE TABLE orders (
                id INTEGER AUTO_INCREMENT,
                amount DECIMAL(18,2) NOT NULL,
                person_id INT,
                created_at datetime DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                FOREIGN KEY (person_id) REFERENCES people(id),
                CHECK(amount>0)
          );
  CREATE TABLE profiles (
              id INTEGER AUTO_INCREMENT,
              person_id INT,
              address text,
              updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
              PRIMARY KEY (id),
              FOREIGN KEY (person_id) REFERENCES people(id)
        );
  INSERT INTO `mydb`.`people`
        (`first_name`,
        `second_name`,
        `DOB`)
        VALUES
        ('John',
        'Lennon',
        STR_TO_DATE('1/01/2012', '%d/%m/%Y')),
        ('Han',
        'Solo',
        STR_TO_DATE('1/01/2012', '%d/%m/%Y'));
  INSERT INTO `mydb`.`profiles`
          (
          `person_id`,
          `address`)
          VALUES
          (1, "111 w. maple"),(2, "250 e. chestnut");
  INSERT INTO `mydb`.`orders`
        (`amount`,
        `person_id`)
        VALUES
        (12.02,1), (9.02,1), (13.02,2), (15.02,2), (15.02,2);
  UPDATE `mydb`.`orders`
            SET
            `amount` = 2*amount
            WHERE `id` = 3;