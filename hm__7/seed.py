from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random


from tables import Student, Group, Teacher, Subject, Grade


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

fake = Faker()


groups = []
for _ in range(3):
    group_name = fake.word()
    groups.append(Group(name=group_name))

session.add_all(groups)
session.commit()

teachers = []
for _ in range(5):
    fullname = fake.name()
    teachers.append(Teacher(fullname=fullname))

session.add_all(teachers)
session.commit()


subjects = []
for _ in range(8):
    subject_name = fake.word()
    teacher_id = random.choice(teachers).id
    subjects.append(Subject(name=subject_name, teacher_id=teacher_id))

session.add_all(subjects)
session.commit()


students = []
for _ in range(30):
    fullname = fake.name()
    group_id = random.choice(groups).id
    student = Student(fullname=fullname, group_id=group_id)
    students.append(student)


    for _ in range(random.randint(5, 20)):
        subject_id = random.choice(subjects).id
        grade = random.randint(0, 100)
        grade_date = fake.date()
        student_grade = Grade(
            student_id=student.id,
            subject_id=subject_id,
            grade=grade,
            grade_date=grade_date)
        session.add(student_grade)

session.add_all(students)
session.commit()

session.close()
