from cli.base import BaseCLI
from config.models import Group


class GroupCLI(BaseCLI):
    def create(self, name):
        new_group = Group(name=name)
        self.session.add(new_group)
        self.session.commit()
        print(f'Group created with Name: {name}')

    def list(self):
        groups = self.session.query(Group).all()
        for group in groups:
            print(f'ID: {group.id}, Name: {group.name}')

    def update(self, id, name):
        group = self.session.query(Group).filter_by(id=id).first()
        if group:
            group.name = name
            self.session.commit()
            print(f'Group ID: {id} updated to Name: {name}')
        else:
            print(f'Group with ID: {id} not found')

    def remove(self, id):
        group = self.session.query(Group).filter_by(id=id).first()
        if group:
            self.session.delete(group)
            self.session.commit()
            print(f'Group with ID: {id} has been removed')
        else:
            print(f'Group with ID: {id} not found')
