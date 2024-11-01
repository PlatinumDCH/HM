import logging


from faker import Faker
import random
import psycopg2
from psycopg2 import DatabaseError

from config import SettingsBD
fake = Faker()

# Подключение к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=SettingsBD.HOST.value,
            database=SettingsBD.DATABASE.value,
            user=SettingsBD.USER.value,
            password=SettingsBD.PASSWORD.value
        )
        return conn
    except DatabaseError as err:
        logging.error(f"Error connection: {err}")
        return None


def add_groups(cur, num_groups=3):
    """added groups"""
    for _ in range(num_groups):
        cur.execute("INSERT INTO groups (name) VALUES (%s)", (fake.word(),))

def add_teachers(cur, num_teachers=3):
    """added teachers"""
    for _ in range(num_teachers):
        cur.execute("INSERT INTO teachers (fullname) VALUES (%s)", (fake.name(),))

def add_subjects(cur, num_teachers=3, subjects_per_teacher=2):
    """added subj with anchor teachers"""
    for teacher_id in range(1, num_teachers + 1):
        for _ in range(subjects_per_teacher):
            cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (%s, %s)", (fake.word(), teacher_id))

def add_students_and_grades(cur, num_groups=3, students_per_group=10, subjects_per_student=6, grades_per_subject=3):
    """added student and grades"""
    for group_id in range(1, num_groups + 1):
        for _ in range(students_per_group):
            # added student and get him id
            cur.execute("INSERT INTO students (fullname, group_id) VALUES (%s, %s) RETURNING id",
                        (fake.name(), group_id))
            student_id = cur.fetchone()[0]
            # added grades for subject
            for subject_id in range(1, subjects_per_student + 1):
                for _ in range(grades_per_subject):
                    cur.execute(
                        "INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s)",
                        (student_id, subject_id, random.randint(0, 100), fake.date_this_decade())
                    )


# Основная функция для выполнения всех операций
def populate_database():
    conn = connect_to_db()
    if conn is None:
        return

    cur = conn.cursor()
    try:
        add_groups(cur)
        add_teachers(cur)
        add_subjects(cur)
        add_students_and_grades(cur)

        # Сохраняем изменения
        conn.commit()
        print("DataBase successful fill random data.")
    except DatabaseError as e:
        logging.error(f"Error for execute operation: {e}")
        conn.rollback()
    finally:
        # close connection
        cur.close()
        conn.close()

# Запуск скрипта
if __name__ == "__main__":
    populate_database()