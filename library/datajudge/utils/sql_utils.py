"""
Common SQL utils.
"""
import pyodbc
import sqlalchemy


def get_table(engine: sqlalchemy.engine.Engine,
              table_name: str):
    """
    Return a table from a db.
    """
    return engine.execute("SELECT * FROM {}".format(table_name))


def get_table_dremio(conn: pyodbc.Connection,
                     table_name: str):
    """
    Return a table from a db.
    """
    return conn.execute("SELECT * FROM {}".format(table_name))
