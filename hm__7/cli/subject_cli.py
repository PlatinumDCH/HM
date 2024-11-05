from cli.base import BaseCLI
from config.models import Subject


class SubjectCLI(BaseCLI):
    def create(self, name):
        new_subject = Subject(name=name)
        self.session.add(new_subject)
        self.session.commit()
        print(f'Subject created with Name: {name}')

    def list(self):
        subjects = self.session.query(Subject).all()
        for subject in subjects:
            print(f'ID: {subject.id}, Name: {subject.name}')

    def update(self, id, name):
        subject = self.session.query(Subject).filter_by(id=id).first()
        if subject:
            subject.name = name
            self.session.commit()
            print(f'Subject ID: {id} updated to Name: {name}')
        else:
            print(f'Subject with ID: {id} not found')

    def remove(self, id):
        subject = self.session.query(Subject).filter_by(id=id).first()
        if subject:
            self.session.delete(subject)
            self.session.commit()
            print(f'Subject with ID: {id} has been removed')
        else:
            print(f'Subject with ID: {id} not found')
