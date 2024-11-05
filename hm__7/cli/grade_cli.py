from cli.base import BaseCLI
from config.models import Grade


class GradeCLI(BaseCLI):
    def create(self, student_id, subject_id, grade_value):
        new_grade = Grade(student_id=student_id, subject_id=subject_id, grade_value=grade_value)
        self.session.add(new_grade)
        self.session.commit()
        print(f'Grade created for Student ID: {student_id}, Subject ID: {subject_id}, Grade: {grade_value}')

    def list(self):
        grades = self.session.query(Grade).all()
        for grade in grades:
            print(
                f'ID: {grade.id}, Student ID: {grade.student_id}, Subject ID: {grade.subject_id}, Grade: {grade.grade_value}')

    def update(self, id, grade_value):
        grade = self.session.query(Grade).filter_by(id=id).first()
        if grade:
            grade.grade_value = grade_value
            self.session.commit()
            print(f'Grade ID: {id} updated to Grade: {grade_value}')
        else:
            print(f'Grade with ID: {id} not found')

    def remove(self, id):
        grade = self.session.query(Grade).filter_by(id=id).first()
        if grade:
            self.session.delete(grade)
            self.session.commit()
            print(f'Grade with ID: {id} has been removed')
        else:
            print(f'Grade with ID: {id} not found')
