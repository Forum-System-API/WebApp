from typing import Callable
from storage import TokenStorage


class Action:
    @classmethod
    def default(cls):
        return cls(lambda: print('No such action'), requires_login = False)
    
    def __init__(self, action: Callable, *, requires_login:bool, name=''):
        self._action = action
        self._requires_login = requires_login
        self.name = name
        
        
    def execute(self):
        if self._requires_login:
            token = TokenStorage.load_token()
            if token:
                self._action(token)
            else:
                print('You have to be logged in!')
        else:
            self._action()