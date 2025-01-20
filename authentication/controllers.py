import os
import click
import validators
from core.config_peewee import db
from .models import User
from .auth import AuthManager

import peewee
from peewee import IntegrityError

from passlib.hash import argon2
from dotenv import load_dotenv
from cryptography.fernet import Fernet


class Controllers():
    PASSWORD_KEY = Fernet(os.getenv('PASSWORD_KEY').encode())
    def __init__(self):
        load_dotenv()
        self.user = None
        self.token = AuthManager().token_cache()

        if self.token is not None:
            self.user = User.get_or_none(User.id == self.token["user_id"])



    def login(self, email, password)-> False:
        if self.token:
            click.echo("Vous êtes déjà connecté.")
            return False
        try:
            user = User.get(User.email == email)
            if self.verify_password(user, password):

                AuthManager().token_create(user)
                self.token = AuthManager().token_cache()

                click.echo(f"Connexion réussie!")
                return True
            else:
                click.echo("Mot de passe incorrect.")
        except peewee.DoesNotExist:
            click.echo("Utilisateur non trouvé.")
        except Exception as e:
            click.echo(f"Erreur lors de la connexion : {e}")
        return False

    def verify_password(self, user, verif_password):
        password = self.PASSWORD_KEY.decrypt(user.password.encode())
        ctrl_password = (verif_password + user.salt).encode()
        return argon2.verify(ctrl_password, password)

    """
    Update
    Delete
    """
    @classmethod
    def create(cls, name, email, password, confirm_password, role):

        while password != confirm_password:
            click.echo("Les mots de passe ne correspondent pas.")
            password = click.prompt("Password")
            confirm_password = click.prompt("Confirmez le mot de passe")

        if not validators.email(email):
            click.echo("Email invalide")
            email = click.prompt("Email")

        salt = os.urandom(16).hex()
        password_hash = argon2.hash(password.encode() + salt.encode())
        encrypted_password = cls.PASSWORD_KEY.encrypt(password_hash.encode())

        try:
            with db.atomic():
                user = User.create(name=name, email=email, password=encrypted_password, role=role, salt=salt)
                user.save()
        except IntegrityError as e:
            raise ValueError(f"Erreur d'intégrité des données : {e}")
        return  user