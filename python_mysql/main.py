from database.mysql import MySQLDatabase
from settings import DbSettings
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

if __name__ == "__main__":
    db = MySQLDatabase(DbSettings.get('database_name'),
                       DbSettings.get('username'),
                       DbSettings.get('password'),
                       DbSettings.get('host'))

    results = db.select('people')
    for row in results:
        print(row)
