import argparse
from cli.student_cli import StudentCLI
from cli.teacher_cli import TeacherCLI
from cli.grade_cli import GradeCLI
from cli.subject_cli import SubjectCLI
from cli.group_cli import GroupCLI


def main():
    parser = argparse.ArgumentParser(
        description="CLI [student,teacher,subj,grades,groups]")

    parser.add_argument('--action', '-a', type=str, choices=[
                                                             'create',
                                                             'list',
                                                             'update',
                                                             'remove'
                                                            ], required=True,
                        help='Action')
    parser.add_argument('--model', '-m', type=str, choices=[
                                                                'Student',
                                                                'Teacher',
                                                                'Grade',
                                                                'Subject',
                                                                'Group'],
                        required=True, help='Model name')
    parser.add_argument('--name', type=str, help='Имя')
    parser.add_argument('--id', type=int, help='ID')
    parser.add_argument('--student_id', type=int, help='ID student')
    parser.add_argument('--subject_id', type=int, help='ID subj')
    parser.add_argument('--grade_value', type=int, help='grade value')

    args = parser.parse_args()

    if args.model == 'Student':
        cli = StudentCLI()
    elif args.model == 'Teacher':
        cli = TeacherCLI()
    elif args.model == 'Grade':
        cli = GradeCLI()
    elif args.model == 'Subject':
        cli = SubjectCLI()
    elif args.model == 'Group':
        cli = GroupCLI()
    else:
        print('Unknown model')
        return

    if args.action == 'create':
        if args.model in ['Student', 'Teacher', 'Subject', 'Group'] and not args.name:
            print(f"For create obj {args.model} need input name with param --name")
            return
        elif args.model == 'Grade' and (not args.student_id or not args.subject_id or args.grade_value is None):
            print("For create obj Grade need input student_id, subject_id and grade_value")
            return

        if args.model == 'Student':
            cli.create(fullname=args.name)
        elif args.model == 'Teacher':
            cli.create(fullname=args.name)
        elif args.model == 'Subject':
            cli.create(name=args.name)
        elif args.model == 'Group':
            cli.create(name=args.name)
        elif args.model == 'Grade':
            cli.create(student_id=args.student_id, subject_id=args.subject_id, grade_value=args.grade_value)
    elif args.action == 'list':
        cli.list()
    elif args.action == 'update':
        if not args.id or (args.model in ['Student', 'Teacher', 'Subject', 'Group'] and not args.name):
            print(
                f"For reload obj {args.model} need input ID and new name with  param --id and --name")
            return
        elif args.model == 'Grade' and (args.grade_value is None):
            print(
                "For reload obj Grade need input ID and new grade with param --id and --grade_value")
            return

        if args.model == 'Student':
            cli.update(id=args.id, fullname=args.name)
        elif args.model == 'Teacher':
            cli.update(id=args.id, fullname=args.name)
        elif args.model == 'Subject':
            cli.update(id=args.id, name=args.name)
        elif args.model == 'Group':
            cli.update(id=args.id, name=args.name)
        elif args.model == 'Grade':
            cli.update(id=args.id, grade_value=args.grade_value)
    elif args.action == 'remove':
        if not args.id:
            print(f"For del obj {args.model} need input ID with param --id")
            return
        cli.remove(id=args.id)
    else:
        print("Unknown action")


if __name__ == "__main__":
    main()
