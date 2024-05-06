from os import remove

class TokenStorage:
    _TOKEN_FILE = 'token.txt'
    _token = None
    
    @classmethod
    def save_token(cls, token):
        with open(cls._TOKEN_FILE, 'w') as f:
            cls._token = token
            f.write(token)
            
    @classmethod
    def load_token(cls):
        
        if cls._token is not None:
            return cls._token
        else:
            try:
                with open (cls._TOKEN_FILE, 'r') as f:
                    cls._token = f.read()
                return cls._token
            except:
                return None
            
    @classmethod
    def delete_token(cls):
        cls._token = None
        remove(cls._TOKEN_FILE)
                    
        
        