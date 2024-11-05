from sqlalchemy import func

from config.models import Student, Grade, Subject
from config.data_base import session


def extra_select_1(teacher_id, student_id):
    """Returns the average grade that the teacher (
        teacher_id) gives to the student (student_id)"""
    result = session.query(func.avg(Grade.grade).label('average_grade')). \
        join(Subject, Grade.subjects_id == Subject.id). \
        filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id). \
        scalar()

    return result


def extra_select_2(group_id, subject_id):
    # Возвращает оценки студентов в группе (group_id) по предмету (subject_id) за последнее занятие
    subquery = session.query(func.max(Grade.date_of)). \
        join(Student, Grade.student_id == Student.id). \
        filter(Student.group_id == group_id, Grade.subjects_id == subject_id). \
        subquery()

    result = session.query(Grade). \
        join(Student, Grade.student_id == Student.id). \
        filter(Student.group_id == group_id, Grade.subjects_id == subject_id, Grade.date_of == subquery.c[0]). \
        all()

    return result

def printing_select_1(teacher_id, student_id):
    average_grade = extra_select_1(teacher_id, student_id)
    if average_grade is not None:
        print(f"AVG grade,  teacher (ID: {teacher_id}) get student (ID: {student_id}):")
        print(f"    {average_grade:.2f}\n")
    else:
        print("Not found data\n")


def printing_select_2(group_id, subject_id):
    grades = extra_select_2(group_id, subject_id)
    print(f"Grades students in group (ID: {group_id}) in subj (ID: {subject_id}) for last class_work:")
    if grades:
        for grade in grades:
            print(f"    Studen (ID: {grade.student_id}), Grade: {grade.grade}, Date: {grade.date_of}")
    else:
        print("    Not found data.\n")


if __name__ == "__main__":
    teacher_id = 1
    student_id = 1
    group_id = 1
    subject_id = 1

    print("=== Extra select ===")
    printing_select_1(teacher_id, student_id)
    printing_select_2(group_id, subject_id)



