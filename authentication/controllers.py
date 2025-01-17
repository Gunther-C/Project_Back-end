import os
import validators
from core.config_peewee import db
from authentication.models import User
from peewee import IntegrityError
from passlib.hash import argon2
from dotenv import load_dotenv
from cryptography.fernet import Fernet


class Controllers():
    def __init__(self):
        load_dotenv()
        self.password_key = Fernet(os.getenv('PASSWORD_KEY').encode())
        self.user = None

    def create(self, **kwargs):
        for key in kwargs:
            if not kwargs[key]:
                raise ValueError("Vous devez remplir tous les champs")

        name = kwargs["name"]
        email = kwargs["email"]
        password = kwargs["password"]
        confirm_password = kwargs["confirm_password"]
        role = kwargs["role"]

        if password != confirm_password:
            raise ValueError("Les mots de passe ne correspondent pas")
        if not validators.email(email):
            raise ValueError("Email invalide")

        salt = os.urandom(16).hex()
        password_hash = argon2.hash(password.encode() + salt.encode())
        encrypted_password = self.password_key.encrypt(password_hash.encode())

        try:
            with db.atomic():
                self.user = User.create(name=name, email=email, password=encrypted_password, role=role, salt=salt)
                self.user.save()
        except IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité des données : {e}")
        return  self.user


    def verify_password(self, user, verif_password):
        password = self.password_key.decrypt(user.password.encode())
        ctrl_password = (verif_password + user.salt).encode()
        return argon2.verify(ctrl_password, password)

    """
    Update
    Delete
    """