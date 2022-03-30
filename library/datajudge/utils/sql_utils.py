"""
Common SQL utils.
"""
import sqlalchemy


def get_table(engine: sqlalchemy.engine.Engine,
              table_name: str):
    return engine.execute("SELECT * FROM {}".format(table_name))
