from config.data_base import engine, session
from config.models import Base, Teacher, Grade, Subject, Student, Group


def create_tables():
    Base.metadata.create_all(engine)
    print("Done")

if __name__ == '__main__':
    create_tables()