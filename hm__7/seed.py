import random
from faker import Faker

from config.data_base import engine,session
from config.models import Teacher, Group, Student, Subject, Grade, Base


fake = Faker()

def create_groups():
    groups = []
    for _ in range(3):
        group = Group(name=fake.word().capitalize())
        groups.append(group)
    session.add_all(groups)
    session.commit()
    return groups

def create_teachers():
    teachers = []
    for _ in range(random.randint(3, 5)):
        teacher = Teacher(fullname=fake.name())
        teachers.append(teacher)
    session.add_all(teachers)
    session.commit()
    return teachers

def create_subjects(teachers):
    subjects = []
    for _ in range(random.randint(5, 8)):
        subject = Subject(name=fake.word().capitalize(), teacher_id=random.choice(teachers).id)
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()
    return subjects

def create_students(groups):
    students = []
    for _ in range(random.randint(30, 50)):
        student = Student(fullname=fake.name(), group_id=random.choice(groups).id)
        students.append(student)
    session.add_all(students)
    session.commit()
    return students

def create_grades(students, subjects):
    for student in students:
        for _ in range(random.randint(5, 20)):
            grade = Grade(
                grade=random.randint(1, 100),
                date_of=fake.date(),
                student_id=student.id,
                subjects_id=random.choice(subjects).id
            )
            session.add(grade)
    session.commit()

def main():
    groups = create_groups()
    teachers = create_teachers()
    subjects = create_subjects(teachers)
    students = create_students(groups)
    create_grades(students, subjects)
if __name__ == '__main__':
    main()
