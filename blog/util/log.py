import logging

logger = logging.getLogger(__name__)

def log_postgresql_exception(err, err_location):

    error_str = f"Error in postgresql: {err} at {err_location}"
    logger.error(error_str)
    return error_str