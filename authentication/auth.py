import os
import secrets
import jwt
import diskcache as dc

from core.config_keys import jwt_key

from passlib.hash import argon2
from cryptography.fernet import Fernet
from dotenv import load_dotenv


class AuthManager:
    def __init__(self):
        load_dotenv()
        self.cache = dc.Cache('cache_dir')
        self.key = os.getenv('SECRET_KEY')

    def token_cache(self):
        token = self.cache.get("jwt_token")

        if token is not None:
            try:
                self.token = jwt.decode(token, self.key, algorithms=["HS256"])
                return self.token
            except jwt.InvalidTokenError:
                print("Le token est invalide")
        return None

    def token_create(self, user=None):
        if user is not None:
            payload = {"user_id": str(user.id)}
            token = jwt.encode(payload, self.key, algorithm="HS256")
            self.cache.set("jwt_token", token)

    def token_delete(self):
        self.cache.delete("jwt_token")
