from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tables import Group, Student, Teacher, Subject, Grade
from config import SettingsBD
import random

host = SettingsBD.HOST.value
db = SettingsBD.DATABASE.value
user = SettingsBD.USER.value
password = SettingsBD.PASSWORD.value

engine = create_engine(f'postgresql://{user}:{password}@{host}/{db}')
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

def create_groups():
    groups = [Group(name=f"Group {i+1}") for i in range(3)]
    session.add_all(groups)
    session.commit()
    return groups

def create_teachers():
    teachers = [Teacher(fullname=fake.name()) for _ in range(5)]
    session.add_all(teachers)
    session.commit()
    return teachers

def create_subjects(teachers):
    subjects = [Subject(name=fake.word().capitalize(), teacher_id=random.choice(teachers).id) for _ in range(6)]
    session.add_all(subjects)
    session.commit()
    return subjects

def create_students(groups):
    students = [Student(fullname=fake.name(), group_id=random.choice(groups).id) for _ in range(40)]
    session.add_all(students)
    session.commit()
    return students

def create_grades(students, subjects):
    for student in students:
        for subject in subjects:
            # Генерация 10-20 случайных оценок за разные даты
            for _ in range(random.randint(10, 20)):
                grade = Grade(
                    student_id=student.id,
                    subject_id=subject.id,
                    grade=random.randint(50, 100),
                    grade_date=fake.date_between(start_date="-1y", end_date="today")
                )
                session.add(grade)

    session.commit()

def main():
    # delete all data in table fill
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()
    session.commit()

    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    students = create_students(groups)
    create_grades(students, subjects)

if __name__ == '__main__':
    main()
    session.close()
