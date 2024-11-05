from cli.base import BaseCLI
from config.models import Student


class StudentCLI(BaseCLI):
    def create(self, fullname):
        new_student = Student(fullname=fullname)
        self.session.add(new_student)
        self.session.commit()
        print(f'Student created with Name: {fullname}')

    def list(self):
        students = self.session.query(Student).all()
        for student in students:
            print(f'ID: {student.id}, Name: {student.fullname}')

    def update(self, id, fullname):
        student = self.session.query(Student).filter_by(id=id).first()
        if student:
            student.fullname = fullname
            self.session.commit()
            print(f'Student ID: {id} updated to Name: {fullname}')
        else:
            print(f'Student with ID: {id} not found')

    def remove(self, id):
        student = self.session.query(Student).filter_by(id=id).first()
        if student:
            self.session.delete(student)
            self.session.commit()
            print(f'Student with ID: {id} has been removed')
        else:
            print(f'Student with ID: {id} not found')
