import os
import click
import validators
from core.config_peewee import db
from .models import User

import peewee
from peewee import IntegrityError

from passlib.hash import argon2
from dotenv import load_dotenv
from cryptography.fernet import Fernet



class Controllers():
    def __init__(self):
        load_dotenv()
        self.password_key = Fernet(os.getenv('PASSWORD_KEY').encode())
        self.user = None

    def create(self, name, email, password, confirm_password, role):

        while password != confirm_password:
            click.echo("Les mots de passe ne correspondent pas.")
            password = click.prompt("Password")
            confirm_password = click.prompt("Confirmez le mot de passe")

        if not validators.email(email):
            click.echo("Email invalide")
            email = click.prompt("Email")

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

    def login(self, email, password):
        try:
            user = User.get(User.email == email)
            if self.verify_password(user, password):
                """
                Création du token
                """
                click.echo(f"Connexion réussie!")
                return True
            else:
                click.echo("Mot de passe incorrect.")
        except peewee.DoesNotExist:
            click.echo("Utilisateur non trouvé.")
        except Exception as e:
            click.echo(f"Erreur lors de la connexion : {e}")

    def verify_password(self, user, verif_password):
        password = self.password_key.decrypt(user.password.encode())
        ctrl_password = (verif_password + user.salt).encode()
        return argon2.verify(ctrl_password, password)

    """
    Update
    Delete
    """