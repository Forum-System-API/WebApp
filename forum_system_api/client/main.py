import commands.users as users
from storage import TokenStorage


def welcome_prompt():
    token = TokenStorage.load_token()

    if not token:
        print('Hello, please [L]ogin or [R]egister!')
        choice = input().upper()

        if choice == 'L':
            users.login()
        elif choice == 'R':
            users.register()
        else:
            welcome_prompt()

    else:
        print('Hello, ', end='')
        users.info(token)


def main():
    welcome_prompt()
    print(
        'Commands = [U]sers / [C]ategories / [M]essages / [R]eply / [T]opics')
    choice = input().upper()

    if choice == 'U':
        users.select_action()
    if choice == 'C':
        raise NotImplementedError()  # TO BE IMPLEMENTED
    if choice == 'M':
        raise NotImplementedError()  # TO BE IMPLEMENTED
    if choice == 'R':
        raise NotImplementedError()  # TO BE IMPLEMENTED
    if choice == 'T':
        raise NotImplementedError()  # TO BE IMPLEMENTED


if __name__ == '__main__':
    main()