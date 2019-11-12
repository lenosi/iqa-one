class User(object):

    def __init__(self, username: str, password: str, **kwargs):
        self.username: str = username
        self.password: str = password
        self.kwargs = kwargs
        self.roles: list = []

        if self.kwargs.get('roles') is not None:
            self.roles = self.kwargs.get('roles')
