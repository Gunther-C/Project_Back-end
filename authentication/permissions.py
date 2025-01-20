import click
from functools import wraps
from .auth import AuthManager
from .models import User


class Permissions:
    def __init__(self):
        self.token = AuthManager().token_cache()
        self.user = None

        if self.token is not None:
            self.user = User.get_or_none(User.id == self.token["user_id"])

    def is_authenticated(self):
        return self.user is not None

    def has_role(self, role):
        return self.user and self.user.role == role
