from commands import execute_command


def main():
    run = True
    while run:
        input_user = input('Enter command: ').strip()

        if input_user.lower() == 'exit':
            run = False
            continue

        if ':' not in input_user:
            print('Invalid input format. Expected "command: value"')
            continue

        command, value = [part.strip() for part in input_user.split(':', maxsplit=1)]
        execute_command(command, value)


if __name__ == '__main__':
    main()
