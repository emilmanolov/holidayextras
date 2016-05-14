import config
import sqlite3

def get_db_connection():
    """ Factory function for creating database connection. """
    db = sqlite3.connect(config.PERSISTENCE_LOCATION, check_same_thread=False)
    db.isolation_level = None
    db.row_factory = sqlite3.Row
    return db
