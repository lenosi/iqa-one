from typing import Any, Optional


class User(object):

    def __init__(self, username: str, password: str, **kwargs):
        self.username: str = username
        self.password: str = password
        self.kwargs = kwargs
        self.roles: Optional[Any] = []  # type returned by kwargs.get

        if self.kwargs.get('roles') is not None:
            self.roles = self.kwargs.get('roles')
