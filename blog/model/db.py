import psycopg2
import psycopg2.extras as extras
import psycopg2.sql as sql
from dynaconf import settings

HOST = settings.DBSERVER

class Database:

	def __init__(
		self, 
		user, 
		password, 
		host, 
		port,
		table
	):

		self.user = user
		self.password = password
		self.host = host
		self.port = port  
		self.table = table
		self.dbname = settings.DBNAME
		self._conn = None
		self._cursor = None
   
	def connect(self):
		try:
			self._conn = psycopg2.connect(
				host=self.host,
				database=self.dbname,
				user=self.user,
				password=self.password
			)
			self._conn.autocommit = True
			self._cursor = self._conn.cursor()
		except (Exception, psycopg2.Error) as error:
			raise Exception(error)
   
	def _check_conn(self):
		if not self._conn:
			raise Exception('ERROR: Not connected to database')

	def close_conn(self):
		self._check_conn()
		self._cursor.close()
		self._conn.close()

	@property
	def cursor(self):
		return self._cursor

	def execute(self, sql_query, data = None):
		"""Single row execution."""
		self._check_conn()
		try:
			if data == None:
				self._cursor.execute(sql_query)
				print( '-# ' + sql_query.as_string(self._connection) + ';\n' )
			else:
				self._cursor.execute(sql_query, data)
				print( '-# ' + sql_query.as_string(self._connection) % data + ';\n' )
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception(f'ERROR: {error}')
	
	def _execute_values(self, sql_query, data):
		"""Multiple rows execution."""
		self._check_conn()
		try:
			extras._execute_values(self._cursor, sql_query, data)
			print( '-# ' + sql_query.as_string(self._connection) % data + ';\n' )
		except (Exception, psycopg2.DatabaseError) as error:
			raise Exception(f'ERROR: {error}')
  
   
   	# For each check if single item query or multiple
   	# Then separate function for each

	def insert(self, columns, rows=None):
		# Columns is a dictionary where keys are the column names and values are column type
		insert_query  = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join( map( sql.Identifier, columns ) ),
            sql.SQL(', ').join(sql.Placeholder() * len(rows[0]))
        )
		if rows:
			for row in rows:
				row = tuple(row)
				self.execute(insert_query, row)
		else:
			tuple_to_insert = tuple(columns.values())
			self.execute(insert_query, tuple_to_insert)
	
	def select(self):
		pass
	
	def update(self):
		pass
	
	def delete(self):
		pass
