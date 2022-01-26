import psycopg2
import psycopg2.extras as extras
import psycopg2.sql as sql

from db import Database

class CreateTable:

    def __init__(
        self, 
		user, 
		password, 
		host, 
		port,
		table
    ):
        self._db_obj = Database(user, password, host, port, table)
        self._cursor = self._db_obj.connect().cursor()

    def _create_table(self, sql_statement):
        self._db_obj.execute(sql_statement)
        
    def _check_table(self):
        
        check_table_query = sql.SQL(
			"SELECT EXISTS (SELECT FROM {} WHERE {} LIKE {} AND {} LIKE {} AND {} = {})"
		).format(
			sql.Identifier('information_schema', 'tables'),
			sql.Identifier('table_schema'),
			sql.Literal('public'),
			sql.Identifier('table_type'),
			sql.Literal('BASE TABLE'),
			sql.Identifier('table_name'),
			sql.Literal(self.table)
		)
        self._db_obj.execute(check_table_query)
        return self._cursor.fetchall()[0][0]
    
    def init_tables(self):

        pass
        # No need to check if table exists as it is checked in sql Query

    def _create_blog_table(self):

        sql_statement = "CREATE TABLE IF NOT EXISTS blog \
                        ();"

        pass