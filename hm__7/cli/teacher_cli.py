from cli.base import BaseCLI
from config.models import Teacher


class TeacherCLI(BaseCLI):
    def create(self, fullname):
        new_teacher = Teacher(fullname=fullname)
        self.session.add(new_teacher)
        self.session.commit()
        print(f'Teacher created with Name: {fullname}')

    def list(self):
        teachers = self.session.query(Teacher).all()
        for teacher in teachers:
            print(f'ID: {teacher.id}, Name: {teacher.fullname}')

    def update(self, id, fullname):
        teacher = self.session.query(Teacher).filter_by(id=id).first()
        if teacher:
            teacher.fullname = fullname
            self.session.commit()
            print(f'Teacher ID: {id} updated to Name: {fullname}')
        else:
            print(f'Teacher with ID: {id} not found')

    def remove(self, id):
        teacher = self.session.query(Teacher).filter_by(id=id).first()
        if teacher:
            self.session.delete(teacher)
            self.session.commit()
            print(f'Teacher with ID: {id} has been removed')
        else:
            print(f'Teacher with ID: {id} not found')
