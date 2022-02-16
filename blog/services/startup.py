from blog.config.config import Settings

from blog.util.log import log_postgresql_exception
from blog.model.create_table import CreateTable

settings = Settings()
HOST = settings.db_server
USER = settings.db_user
PASSWORD = settings.db_pwd
PORT = settings.db_port


def init_db():
    
    # TODO: If create table returns false, drop all tables

    try:
        create_table_obj = CreateTable(USER, PASSWORD, HOST, PORT)
        result = create_table_obj.init_tables()
        return True, None

    except Exception as e:
        error_location = 'blog.services.startup: init_db'
        error_str = log_postgresql_exception(e, error_location)
        return False, error_str
