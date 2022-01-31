import psycopg2
import psycopg2.sql as sql
from blog.model.create_table import CreateTable
from blog.model.db import Database

host = '127.0.0.1'
user = 'postgres'
pwd = 'admin'
dbname = 'blogdb'
port = '5432'

# def connect():
#     try:
#         conn = psycopg2.connect(
#             host=host,
#             database=dbname,
#             user=user,
#             password=pwd
#         )
#         conn.autocommit = True
#         cursor = conn.cursor()
#         return conn, cursor
#     except (Exception, psycopg2.Error) as error:
#         raise Exception(error)

# columns = ['id Serial Primary Key ','Person int', 'Name varchar(255)']

# # create_table_query = f"CREATE TABLE {'blog'} (id serial PRIMARY KEY, num integer, data varchar);"

# conn, cursor = connect()
# # # print(create_table_query.as_string(conn))
# # cursor.execute(create_table_query)
# # help(cursor.execute)

# table_name = 'blog'
# check_table_query = sql.SQL(
# 	"SELECT EXISTS (SELECT FROM {} WHERE {} LIKE {} AND {} LIKE {} AND {} = {})"
# 	).format(
#         sql.Identifier('information_schema', 'tables'),
#         sql.Identifier('table_schema'),
#         sql.Literal('public'),
#         sql.Identifier('table_type'),
#         sql.Literal('BASE TABLE'),
#         sql.Identifier('table_name'),
#         sql.Literal(table_name)
# 	)
# print(f"Query: {check_table_query.as_string(conn)}")
# cursor.execute(check_table_query)
# print(cursor.fetchall()[0][0])

table = 'post'
# create_table_obj = CreateTable(user, pwd, host, port, table)
# print(create_table_obj.create_post_table())
# print(create_table_obj.check_table())
# print(create_table_obj.init_tables()) 


db_obj = Database(user, pwd, host, port, table)
post_columns = {
    'content': 'Hello World',
    'links': 'http://localhost',
    'title': 'Hello World',
    'published_at': '1/31/2022',
    'images': 'file_location' 
}
db_obj.connect()
db_obj.insert(**post_columns)