import psycopg2
from config import SettingsBD


def execute_query(query_file, params=None):
    with open(query_file, 'r') as file:
        sql = file.read()
    with psycopg2.connect(
        host=SettingsBD.HOST.value,
        database=SettingsBD.DATABASE.value,
        user=SettingsBD.USER.value,
        password=SettingsBD.PASSWORD.value
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

def get_average_grade(student_id, teacher_id):
    results = execute_query('query_11.sql', (student_id, teacher_id))
    return results

if __name__ == "__main__":
    student_id = 1
    teacher_id = 2
    average_grade = get_average_grade(student_id, teacher_id)

    for row in average_grade:
        print(f"Average grade for student ID {student_id} by teacher ID {teacher_id}: {row[0]}")