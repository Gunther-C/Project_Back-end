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


    def token_existing(self):
        token = self.cache.get("jwt_token")
        if token:
            try:
                return jwt.decode(token, self.key, algorithms=["HS256"])
            except jwt.InvalidTokenError:
                print("Le token est invalide")
        return None


    def token_create(self):
        """
        Creation of the JWT
        :return: Token
        """
        payload = {"user_id": self.user.id}
        token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
        CACHE_KEY.set("jwt_token", token)

    def token_delete(self):
        cache.delete("jwt_token")
