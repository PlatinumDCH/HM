from sqlalchemy import func

from config.models import Student, Grade, Subject,Teacher, Group
from config.data_base import session


def get_top_students():
    """
    report_1
    Find the top 5 students with the highest average grade across all subjects.
    """
    subquery = session.query(
        Grade.student_id,
        func.avg(Grade.grade).label('average_grade')
    ).group_by(Grade.student_id).subquery()

    top_students = session.query(
        Student.name,
        subquery.c.average_grade
    ).join(
        subquery, Student.id == subquery.c.student_id
    ).order_by(
        subquery.c.average_grade.desc()
    ).limit(5).all()

    return top_students


def get_top_students_in_subject(subject_id):
    """
    report_2
    Find student with height avg grade in selection subj.
    """
    top_student = session.query(
        Student.fullname,
        func.avg(Grade.grade).label('average_grade')
    ).join(Grade).filter(
        Grade.subjects_id == subject_id
    ).group_by(
        Grade.student_id, Student.fullname
    ).order_by(
        func.avg(Grade.grade).desc()
    ).first()

    return top_student


def get_average_grade_in_groups(subject_id):
    """
    report_3
    Find avg grade in group in select subj.
    """
    average_grades = session.query(
        Group.name,
        func.avg(Grade.grade).label('average_grade')
    ).join(Student, Group.id == Student.group_id).join(Grade, Student.id == Grade.student_id).filter(
        Grade.subjects_id == subject_id
    ).group_by(
        Group.id, Group.name
    ).all()

    return average_grades


def get_average_grade_in_all():
    """
    report_4
    Find avg grade in all table_avg.
    """
    average_grade = session.query(
        func.avg(Grade.grade).label('average_grade')
    ).scalar()

    return average_grade


def get_courses_by_teacher(teacher_id):
    """
    report_5
    Find witch subj learn select t.
    """
    courses = session.query(
        Subject.name
    ).join(Subject.teacher).filter(
        Teacher.id == teacher_id
    ).all()

    return courses


def get_students_in_group(group_id):
    """
    report_6
    Find list s in select g.
    """
    students = session.query(
        Student.fullname
    ).filter(
        Student.group_id == group_id
    ).all()

    return students


def get_grades_in_group_subject(group_id, subject_id):
    """
    report_7
    Find grades s in select g in select sbj.
    """
    grades = session.query(
        Student.fullname,
        Grade.grade
    ).join(Grade).filter(
        Student.group_id == group_id,
        Grade.subjects_id == subject_id
    ).all()

    return grades


def get_average_grade_by_teacher(teacher_id):
    """
    report_8
    Find abg grade t.
    """
    average_grade = session.query(
        func.avg(Grade.grade).label('average_grade')
    ).join(Subject).join(Subject.teacher).filter(
        Teacher.id == teacher_id
    ).scalar()

    return average_grade


def get_courses_by_student(student_id):
    """
    report_9
    Find all c student.
    """
    courses = session.query(
        Subject.name
    ).join(Grade).filter(
        Grade.student_id == student_id
    ).all()

    return courses


def get_courses_by_student_and_teacher(student_id, teacher_id):
    """
    report_10
    The list of courses taught by a certain teacher to a certain student.
    """
    courses = session.query(
        Subject.name
    ).join(Grade).join(Subject.teacher).filter(
        Grade.student_id == student_id,
        Teacher.id == teacher_id
    ).all()

    return courses


if __name__ == '__main__':
    subject_id = 1
    teacher_id = 1
    student_id = 1
    group_id = 1

    print("=== +++ ===")
    print(f"1. Лучшие студенты по предмету (ID: {subject_id}):")
    print(f"   {get_top_students_in_subject(subject_id)}\n")

    print("2. Средний балл по группам для предмета:")
    print(f"   {get_average_grade_in_groups(subject_id)}\n")

    print("3. Средний балл по всем предметам:")
    print(f"   {get_average_grade_in_all()}\n")

    print(f"4. Курсы, преподаваемые учителем (ID: {teacher_id}):")
    print(f"   {get_courses_by_teacher(teacher_id)}\n")

    print(f"5. Студенты в группе (ID: {group_id}):")
    print(f"   {get_students_in_group(group_id)}\n")

    print(f"6. Оценки по предмету (ID: {subject_id}) в группе (ID: {group_id}):")
    print(f"   {get_grades_in_group_subject(group_id, subject_id)}\n")

    print(f"7. Средний балл, выставленный учителем (ID: {teacher_id}):")
    print(f"   {get_average_grade_by_teacher(teacher_id)}\n")

    print(f"8. Курсы, которые посещает студент (ID: {student_id}):")
    print(f"   {get_courses_by_student(student_id)}\n")

    print(f"9. Курсы, посещаемые студентом (ID: {student_id}) у учителя (ID: {teacher_id}):")
    print(f"   {get_courses_by_student_and_teacher(student_id, teacher_id)}\n")

