import requests
from config import BASE_URL
from storage import TokenStorage
# from views import user_view
from commands.action import Action

USERS_URL = f'{BASE_URL}/users'


def login():
    data = {
        'username': input('Username = '),
        'password': input('Password = ')
    }

    response = requests.post(f'{USERS_URL}/login', json=data)

    if response.status_code == 200:
        token = response.json()['token']
        TokenStorage.save_token(token)
        print('Successfully logged in!')
    else:
        print('Invalid login attempt')
        login()


def logout(token):
    TokenStorage.delete_token()


def info(token):
    response = requests.get(f'{USERS_URL}/info', headers={'x-token': token})

    if response.status_code == 200:
        print(response.json())
    else:
        print(response.text)


def register():
    data = {
        'username': input('Username = '),
        'password': input('Password = ')
    }
    
    
    response = requests.post(f'{USERS_URL}/register', json=data)

    if response.status_code == 200:
        print('Successfully registered!')
        print(response.json())
    else:
        print(response.text)


# to show all the conversations
# all replies

def select_action():
    actions = {
        'IN': Action(login, requires_login=False, name ='log[IN]'),
        'OUT': Action(logout, requires_login=True, name ='log[OUT]'),
        'I': Action(info, requires_login=True, name='log[I]'),
        'R': Action(register, requires_login=False, name = 'log[R]')
        # to show all the conversations
        # all replies
    }
    
    print('Select user action?')
    print('/'.join(action.name for action in actions.values()))
    
    select_action = input().upper()
    actions.get(select_action, Action.default()).execute()
