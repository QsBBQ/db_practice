
from database.mysql import MySQLDatabase
from settings import DbSettings
import datetime

# note to self would like to add tests and logging
# MySQLDatabase().get_available_tables()
# MySQLDatabase().get_columns_for_table("profiles")
# MySQLDatabase().get_columns_for_table("orders")
# MySQLDatabase().get_columns_for_table("articles")
#
# MySQLDatabase().select("profiles")
# MySQLDatabase().select("people", ["first_name", "second_name"])
# MySQLDatabase().select("orders", [], where ="amount > 9")
# MySQLDatabase().select("people", [], join = "orders on people.id = orders.person_id")
# MySQLDatabase().select("people", [], True, limit = "1")
# MySQLDatabase().select("orders", [], order_by = "amount")
# MySQLDatabase().select("orders", [], True, where = "amount > 9", order_by = "amount")
# MySQLDatabase().select("orders", [], True, where = "amount > 9", order_by = "amount", limit = "2")
#MySQLDatabase().delete("orders", id="=10")
#MySQLDatabase().delete("orders", person_id="=3", amount=">8")
#MySQLDatabase().insert("orders", amount="8.1", person_id="3")
#MySQLDatabase().update("orders", where="id=11", amount="9.1")

def person_average(person):
    # review named tuple to be true or false
    person_id = str((db.select("people", ['id'], False, where="first_name='%s'"% person))[0][0])
    print(person_id)
    print(db.select("people",
          ["CONCAT(people.first_name, ' spends') AS First_Name, AVG(amount) AS Average"],
          True,
          join="orders on people.id = orders.person_id",
          where="person_id=%s" % person_id))

def add_person(first_name, last_name, dob):
    # trouble adding dob
    # datetime.datetime.strptime(dob, '%d/%m/%Y')
    db.insert("people",
              first_name=first_name,
              second_name=last_name,
              )
              #dob="STR_TO_DATE('%s', '%%d/%%m/%%Y')" % dob)

def add_profile(first_name, address):
    person_id = str((db.select("people", ['id'], False, where="first_name='%s'"% first_name))[0][0])
    db.insert("profiles",
              person_id=person_id,
              address=address
              )

def add_orders(first_name, amounts):
    person_id = str((db.select("people", ['id'], False, where="first_name='%s'"% first_name))[0][0])
    for amount in amounts:
        db.insert("orders",
                  amount=amount,
                  person_id=person_id)

def person_min(first_name):
    person_id = str((db.select("people", ['id'], False, where="first_name='%s'"% first_name))[0][0])
    print(db.select("orders",
                    ["CONCAT(people.first_name, ' ', people.second_name) AS full_name",
                    "min(amount) AS minimum"],
                    True,
                    join="people on people.id = orders.person_id",
                    where="person_id=%s" % person_id))

def mass_order_update(first_name, amount):
    """Updates all the specified users orders with specified amount"""
    person_id = str((db.select("people", ['id'], False, where="first_name='%s'"% first_name))[0][0])
    db.update("orders",
              where="person_id=%s" % person_id,
              amount=amount)

if __name__ == "__main__":
    db = MySQLDatabase(DbSettings.get('database_name'),
                       DbSettings.get('username'),
                       DbSettings.get('password'),
                       DbSettings.get('host'))

    # Example
    # print(db.select("people",
    #       ["CONCAT(people.first_name, ' spends') AS First_Name, AVG(amount) AS Average"],
    #       True,
    #       join="orders on people.id = orders.person_id",
    #       where="person_id=1"))

    # person_average("han")
    # add_person("Bob","Hope", "1/01/1910")
    # add_profile("Bob", "1 w. washington")
    # add_orders("Bob", ["12.50", "13.50"])
    # person_min("Bob")
    # mass_order_update("Bob", "20.02")
