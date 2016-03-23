import MySQLdb AS _mysql
db = _mysql.CONNECT(db=database_name,
                    host=host,
                    USER=username,
                    passwd=password)

cursor = db.cursor()
cursor.EXECUTE("SELECT * FROM my_table;")

results = cursor.fetchall()

cursor.close()
