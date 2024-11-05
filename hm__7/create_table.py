from config.data_base import engine
from config.models import Base


def create_tables():
    """
    Creates all tables defined in the Base metadata.

    Calls the SQLAlchemy `create_all` method, which creates
    all tables that do not already exist in the database according
    to the schema defined in the `Base` metadata. Also prints a
    confirmation message upon successful creation of the tables.
    """
    Base.metadata.create_all(engine)
    print("Done")

if __name__ == '__main__':
    create_tables()