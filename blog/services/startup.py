from dynaconf import settings
from blog.util.log import log_postgresql_exception
from blog.model.create_table import CreateTable

HOST = settings.DBSERVER
USER = settings.DBUSER
PASSWORD = settings.DBPWD
PORT = settings.DBPORT


def init_db():
    
    # TODO: If create table returns false, drop all tables

    try:
        create_table_obj = CreateTable(USER, PASSWORD, HOST, PORT)
        result = create_table_obj.init_tables()

    except Exception as e:
        error_location = 'blog.services.startup: init_db'
        error_str = log_postgresql_exception(e, error_location)
        raise Exception(error_str)
