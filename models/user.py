class User:
    def __init__(self):
        self.id = None
        self.email = None
        self.forename = None
        self.surname = None
        self.created = None

class UserValidator(object):
    def validate(self, user):
        pass

class UserDataProvider:

    def __init__(self, args):
        self.db = args
        self.user_id = None
        self.email = None
        self.forename = None
        self.surname = None
        self.created = None

class UserModel:
    __modelname__ = 'user'
    id = None
    email = None
    forename = None
    surname = None
    created = None
