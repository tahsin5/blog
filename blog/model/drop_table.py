import psycopg2
import psycopg2.extras as extras
import psycopg2.sql as sql

from blog.model.db import Database

class DropTable:

    def __init__(
        self, 
		user, 
		password, 
		host, 
		port,
		table
    ):  
        self._table = table
        self._db_obj = Database(user, password, host, port, table)
        self._conn = self._db_obj.connect()
        self._cursor = self._db_obj.cursor

    def _execute_drop_table(self, sql_statement):
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
			sql.Literal(self._table)
		)
        self._db_obj.execute(check_table_query)
        result = self._cursor.fetchall()
        if result and result != None:
            return result[0][0]
        return False
    
    def drop_all_tables(self):
        
        # TODO: Find better way to call multiple methods
        # TODO Fix issue with metadata table creation
        # TODO Fix issue with comment table creation

        create_tables_method_list = [
                                    self._drop_post_table(),
                                    self._drop_category_table(), 
                                    self._drop_tag_table(),
                                    self._drop_post_category_table(),  
                                    self._drop_post_tag_table(), 
                                    ]
        create_tables_results = [method for method in create_tables_method_list]
        return all(create_tables_results)

        # self._drop_metadata_table()
        # self._drop_comment_table()

    def _drop_post_table(self):

        sql_statement = "CREATE TABLE IF NOT EXISTS post (\
                            post_id serial PRIMARY KEY, \
                            content text, \
                            links varchar,   \
                            title varchar,    \
                            published_at timestamp, \
                            images varchar\
                        );"

        self._execute_drop_table(sql_statement)
        self._table = 'post'
        return self._check_table()
    
    def _drop_category_table(self):

        sql_statement = "CREATE TABLE IF NOT EXISTS category (\
                            cat_id serial PRIMARY KEY, \
                            content text, \
                            title varchar  \
                        );"

        self._execute_drop_table(sql_statement)
        self._table = 'category'
        return self._check_table()
    
    def _drop_tag_table(self):

        sql_statement = "CREATE TABLE IF NOT EXISTS tag (\
                            tag_id serial PRIMARY KEY, \
                            content text, \
                            title varchar  \
                        );"

        self._execute_drop_table(sql_statement)
        self._table = 'tag'
        return self._check_table()
    
    # def _drop_metadata_table(self):

    #     sql_statement = "CREATE TABLE IF NOT EXISTS metadata (\
    #                         meta_id integer PRIMARY KEY, \
    #                         content text, \
    #                         key varchar,    \
    #                         FOREIGN KEY(post_id)   \
    #                             REFERENCES post(post_id)\
    #                             ON UPDATE CASCADE ON DELETE CASCADE\
    #                     );"

    #     self._execute_drop_table(sql_statement)
    #     self._table = 'metadata'
    #     self._check_table()
    
    # def _drop_comment_table(self):

    #     sql_statement = "CREATE TABLE IF NOT EXISTS post_comment (\
    #                         comment_id serial PRIMARY KEY, \
    #                         content text, \
    #                         published_bool boolean, \
    #                         title varchar,    \
    #                         published_at timestamp, \
    #                         FOREIGN KEY(post_id)   \
    #                             REFERENCES post(post_id)\
    #                             ON UPDATE CASCADE ON DELETE CASCADE\
    #                     );"

    #     self._execute_drop_table(sql_statement)
    #     self._table = 'post_comment'
    #     self._check_table()


    def _drop_post_category_table(self):

        sql_statement = "CREATE TABLE IF NOT EXISTS post_category (\
                            post_id integer NOT NULL, \
                            cat_id integer NOT NULL, \
                            PRIMARY KEY(post_id, cat_id), \
                            FOREIGN KEY(cat_id) \
                                REFERENCES category(cat_id)\
                                ON UPDATE CASCADE ON DELETE CASCADE,\
                            FOREIGN KEY (post_id) \
                                REFERENCES post (post_id)\
                                ON UPDATE CASCADE ON DELETE CASCADE\
                            \
                        );"

        self._execute_drop_table(sql_statement)
        self._table = 'post_category'
        return self._check_table()
    
    def _drop_post_tag_table(self):

        sql_statement = "CREATE TABLE IF NOT EXISTS post_tag (\
                            post_id integer NOT NULL, \
                            tag_id integer NOT NULL, \
                            PRIMARY KEY(post_id, tag_id), \
                            FOREIGN KEY(tag_id) \
                                REFERENCES tag(tag_id)\
                                ON UPDATE CASCADE ON DELETE CASCADE,\
                            FOREIGN KEY(post_id) \
                                REFERENCES post(post_id)\
                                ON UPDATE CASCADE ON DELETE CASCADE\
                            \
                        );"

        self._execute_drop_table(sql_statement)
        self._table = 'post_tag'
        return self._check_table()