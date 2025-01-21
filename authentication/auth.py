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
        self.cache_dir = dc.Cache('cache_dir')
        self.key = os.getenv('SECRET_KEY')
        self.cache_jwt =None
        self.token = None

    def token_create(self, user=None):
        if user is not None:
            payload = {"user_id": str(user.id)}
            token = jwt.encode(payload, self.key, algorithm="HS256")
            return self.cache_dir.set("jwt_token", token)
        return None

    def token_cache(self):
        cache_token = self.cache_dir.get("jwt_token")
        if cache_token is not None:
            try:
                self.token = jwt.decode(cache_token, self.key, algorithms=["HS256"])
                return self.token
            except jwt.InvalidTokenError:
                print("Le token est invalide")
        return None

    def token_get(self):
        if self.cache_dir.get("jwt_token"):
            print("La session existe")
        else:
            print("La session n'existe pas")

    def token_delete(self):
        if self.cache_dir.delete("jwt_token"):
            print("La session est supprimer")
        else:
            print("La session n'existe pas")