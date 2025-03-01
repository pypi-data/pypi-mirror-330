class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.token = "your_default_token"

    def set_token(self, token_value):
        self.token = token_value

    def get_token(self):
        return self.token
