import MySQLdb as _mysql
import collections
import re
# import ipdb; ipdb.set_trace()

# ONLY needs TO compile one TIME so we put here!
float_match = re.compile(r'[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?$').match

def is_number(string):
    return bool(float_match(string))

class MySQLDatabase:
    #def __init__(self, database_name="mydb", username="codeuser", password="codeuser456", host='localhost'):
    def __init__(self, database_name, username, password, host):
        try:
            self.db = _mysql.connect(db=database_name,
                                    host=host,
                                    user=username,
                                    passwd=password)

            self.database_name = database_name

            print "Connected to MySQL!"
        except _mysql.Error, e:
            print e

    def __del__(self):
        if hasattr(self,'db'): # close our connection TO free it up IN the pool
            self.db.close()
            print "MySQL Connection closed"


    def get_available_tables(self):
        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES;")

        self.tables = cursor.fetchall()
        # for row in self.tables:
        #     print(row)
        cursor.close()
        return self.tables


    def get_columns_for_table(self, table_name):
        cursor = self.db.cursor()
        cursor.execute("SHOW COLUMNS FROM `%s`" % table_name)

        columns = cursor.fetchall()

        cursor.close()
        # for row in columns:
        #     print(row)
        return columns


    def select(self, table, columns=None, named_tuples=False, **kwargs):
        """
        select(table_name, [list of column names])
        """
        sql_str = "SELECT "

        # ADD COLUMNS OR just the wildcard
        if not columns:
            sql_str += " * "
        else:
            for column in columns:
                sql_str += "%s, " % column
            sql_str = sql_str[:-2] # remove the LAST comma!

        # ADD the TABLE TO SELECT FROM
        sql_str += " FROM `%s`.`%s`" % (self.database_name, table)
        #import ipdb; ipdb.set_trace()
        # there a JOIN clause attached
        if kwargs.has_key('join'):
            sql_str += " JOIN %s" % kwargs.get('join')

        # there a WHERE clause attached
        if kwargs.has_key('where'):
            sql_str += " WHERE %s" % kwargs.get('where')

        # there a ORDER BY clause attached
        if kwargs.has_key('order_by'):
            sql_str += " ORDER BY %s" % kwargs.get('order_by')

        # there a LIMIT clause attached
        if kwargs.has_key('limit'):
            sql_str += " LIMIT %s" % kwargs.get('limit')

        sql_str += ";" # finalise our SQL string

        cursor = self.db.cursor()
        # import ipdb; ipdb.set_trace()
        cursor.execute(sql_str)

        if named_tuples:
            results = self.convert_to_named_tuples(cursor)
        else:
            results = cursor.fetchall()

        cursor.close()
        print(results)
        return results

    def convert_to_named_tuples(self, cursor):
        results = None
        # import ipdb; ipdb.set_trace()
        names = " ".join(d[0] for d in cursor.description)
        klass = collections.namedtuple('Results', names)

        try:
            results = map(klass._make, cursor.fetchall())
        except _mysql.ProgrammingError:
            pass
        # print(results)
        return results

    def delete(self, table, **wheres):
        sql_str = "DELETE FROM `%s`.`%s`" % (self.database_name, table)

        if wheres is not None:
            first_where_clause = True
            for where, term in wheres.iteritems():
                if first_where_clause:
                    # this IS the FIRST WHERE clause
                    sql_str += " WHERE `%s`.`%s`%s" % (table, where, term)
                    print(sql_str)
                    first_where_clause = False
                else:
                    # this IS AND additional clause so USE AND
                    sql_str += " AND `%s`.`%s`%s" % (table, where, term)

        sql_str += ";"

        cursor = self.db.cursor()
        cursor.execute(sql_str)
        self.db.commit()
        cursor.close()

    def insert(self, table, **column_values):
        """
        insert(table_name, **keyword values)
        """
        sql_str = "INSERT INTO `%s`.`%s` " % (self.database_name, table)

        if column_values is not None:
            columns = "("
            values = "("
            for column_name, value in column_values.iteritems():
                columns += "`%s`, " % column_name

                # CHECK how we should ADD this TO the colums string
                if is_number(value):
                    # its a NUMBER so we dont ADD ''
                    values += "%s, " % value
                else:
                    # its a DATE OR a string so ADD the ''
                    values += "'%s', " % value

            columns = columns[:-2] # strip off the spare ', from the end
            values = values[:-2] # same here too

            columns += ") VALUES" # add the connecting key word and brace
            values += ");" # add the brace and like terminator

            sql_str += "%s %s" % (columns, values)


        cursor = self.db.cursor()
        cursor.execute(sql_str)
        self.db.commit()
        cursor.close()

    def update(self, table, where=None, **column_values):
        sql_str = "UPDATE `%s`.`%s` SET " % (self.database_name, table)

        if column_values is not None:
            for column_name, value in column_values.iteritems():
                sql_str += "`%s`=" % column_name

                # CHECK how we should ADD this TO the colums string
                if is_number(value):
                    # its a NUMBER so we dont ADD ''
                    sql_str += "%s, " % value
                else:
                    # its a DATE OR a string so ADD the ''
                    sql_str += "'%s', " % value

        sql_str = sql_str[:-2] # strip off the LAST , AND SPACE CHARACTER

        if where:
            sql_str += " WHERE %s" % where

        cursor = self.db.cursor()
        cursor.execute(sql_str)
        self.db.commit()
        cursor.close()
