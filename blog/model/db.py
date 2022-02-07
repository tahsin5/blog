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
		table = None,
		primary_key = None
	):

		self.user = user
		self.password = password
		self.host = host
		self.port = port  
		self.table = table
		self.dbname = settings.DBNAME
		self.primary_key = primary_key
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
				# print( '-# ' + sql_query.as_string(self._connection) + ';\n' )
			else:
				self._cursor.execute(sql_query, data)
				# print( '-# ' + sql_query.as_string(self._connection) % data + ';\n' )
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

	def insert(self, **column_value):
		insert_query  = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(self.table),
            sql.SQL(', ').join(map(sql.Identifier, column_value.keys())),
            sql.SQL(', ').join(sql.Placeholder() * len(column_value.values()))
        )
		values_to_insert = tuple(column_value.values())
		self.execute(insert_query, values_to_insert)

	def insert_many(self, columns, rows):
		insert_query  = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
			sql.Identifier(self.table),
			sql.SQL(', ').join( map( sql.Identifier, columns ) ),
			sql.SQL(', ').join(sql.Placeholder() * len(rows[0]))
		)
		for row in rows:
			row = tuple(row)
			self.execute(insert_query, row )
	
	def select(self, columns, primary_key_val = None):
		
		if primary_key_val == None:
			select_query = sql.SQL("SELECT {} FROM {}").format(
				sql.SQL(',').join(map(sql.Identifier, columns)),
				sql.Identifier(self.table)
			)
		else:
			select_query = sql.SQL("SELECT {} FROM {} WHERE {} = {}").format(
				sql.SQL(',').join(map(sql.Identifier, columns)),
				sql.Identifier(self.table),
				sql.Identifier(self.primary_key),
				sql.Placeholder()
			)
		
		self.execute(select_query, (primary_key_val,))
		try:
			selected = self._cursor.fetchall()
		except psycopg2.ProgrammingError as error:
			selected = '# ERROR: ' + str(error)
		else:
			print('-# ' + str(selected) + '\n')
			return selected

	def select_all(self, primary_key_val = None):
		
		if primary_key_val == None:
			select_query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table))
			self.execute(select_query)
		else:
			select_query = sql.SQL("SELECT * FROM {} WHERE {} = {}").format(
				sql.Identifier(self.table),
				sql.Identifier(self.primary_key),
				sql.Placeholder()
			)
			self.execute(select_query, (primary_key_val,))
		try:
			selected = self._cursor.fetchall()
		except psycopg2.ProgrammingError as error:
			selected = '# ERROR: ' + str(error)
		else:
			print('-# ' + str(selected) + '\n')
			return selected

	def update(self, columns, primary_key_val):
		
		columns, col_values = list(columns.keys()), list(columns.values())
		update_query  = sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").format(
            sql.Identifier(self.table),
            sql.SQL(',').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(col_values)),
            sql.Identifier(self.primary_key),
            sql.Placeholder()
        )
		placeholder_value = list(col_values)
		placeholder_value.append(primary_key_val)

		self.execute(update_query, (col_values, tuple(placeholder_value)))
	
	def delete(self, primary_key_val = None):
		
		if primary_key_val is None:
			delete_query = sql.SQL("DELETE FROM {}").format(
								   sql.Identifier(self.table))
			self.execute(delete_query)
		
		else:
			delete_query  = sql.SQL("DELETE FROM {} WHERE {} = {}").format(
            	sql.Identifier(self.table),
           		sql.Identifier(self.primary_key),
            	sql.Placeholder()
        	)
			self.execute(delete_query, (primary_key_val,))
