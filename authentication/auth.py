import os
import secrets
import diskcache as dc
# import jwt
from core.config_keys import jwt_key
from passlib.hash import argon2
from cryptography.fernet import Fernet
from dotenv import load_dotenv



class AuthManager:

    def __init__(self, user: object | None = None):
        load_dotenv()

        self.user = user
        self.cache = dc.Cache('cache_dir')
        self.key = os.getenv('JWT_KEY')
        self.token = None

    def token_cache(self):
        token = self.cache.get("jwt_token")
        if token:
            try:
                self.token = jwt.decode(token, self.key, algorithms=["HS256"])
                return self.token
            except jwt.InvalidTokenError:
                print("Le token est invalide")
        return None


    def token_create(self):
        payload = {"user_id": self.user.id}
        self.token = jwt.encode(payload, self.key, algorithm="HS256")
        self.cache.set("jwt_token", self.token)
        return self.token

    def token_delete(self):
        self.cache.delete("jwt_token")
