from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


sql = 'sqlite:///:memory:'
engine = create_engine(sql, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Group(Base):
    __tablename__ = 'groups'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Отношение с таблицей студентов
    students = relationship('Student', back_populates='group', cascade='all, delete-orphan')


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete='CASCADE'))

    # Отношение с таблицей оценок
    grades = relationship('Grade', back_populates='student', cascade='all, delete-orphan')

    # Связь с таблицей групп
    group = relationship('Group', back_populates='students')


class Teacher(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)


    subjects = relationship('Subject', back_populates='teacher', cascade='all, delete-orphan')


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String(175), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id', ondelete='CASCADE'))  # external key on teacher

    # connect with grade-table
    grades = relationship('Grade', back_populates='subject', cascade='all, delete-orphan')

    # connect with teacher-table
    teacher = relationship('Teacher', back_populates='subjects')


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(Integer, primary_key=True)  # Уникальный идентификатор оценки
    student_id = Column(Integer, ForeignKey('students.id', ondelete='CASCADE'))  # external key on student
    subject_id = Column(Integer, ForeignKey('subjects.id', ondelete='CASCADE'))  # external key on subj
    grade = Column(Integer, CheckConstraint('grade >= 0 AND grade <= 100'), nullable=False)  # grade with check
    grade_date = Column(Date, nullable=False)  # date get grade
    # connection to other tables
    student = relationship('Student', back_populates='grades')
    subject = relationship('Subject', back_populates='grades')


# create all tables
Base.metadata.create_all(engine)

if __name__ == '__main__':
    ...

