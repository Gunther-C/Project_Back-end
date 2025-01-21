import os
import click
import validators
from core.config_peewee import db
from .models import User
from .auth import AuthManager
from .permissions import Permissions

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
        self.permission = Permissions()

    def login(self, email, password)-> False:
        user = User.get_or_none(User.email == email)
        if user is None:
            click.echo("Utilisateur non trouvé.")
            return False

        if self.verify_password(user, password):

            AuthManager().token_create(user)

            if self.permission.is_authenticated() is not None:
                self.user = self.permission.user
                return self.user

            click.echo("Authentification à échouée.")
            return False

        click.echo("Mot de passe incorrect.")
        return False

    def verify_password(self, user, verif_password):
        password = self.PASSWORD_KEY.decrypt(user.password.encode())
        ctrl_password = (verif_password + user.salt).encode()
        return argon2.verify(ctrl_password, password)


    def update(self, name, email, password, confirm_password, role):
        if self.user is not None:
            if password:
                while password != confirm_password:
                    click.echo("Les mots de passe ne correspondent pas.")
                    password = click.prompt("Password")
                    confirm_password = click.prompt("Confirmez le mot de passe")

                salt = os.urandom(16).hex()
                password_hash = argon2.hash(password.encode() + salt.encode())
                password = cls.PASSWORD_KEY.encrypt(password_hash.encode())
            else:
                salt = self.user.salt
                password = self.user.password

            if email and not validators.email(email):
                click.echo("Email invalide")
                email = click.prompt("Email")

            """
                ATTENTION permissions.user VA ETRE DIFFERENT DE controller.user
                DECONNEXION ET RECONNEXION NECESSAIRE OU AUTRE
                AVANCER AVEC DEUX OBJECT USER IDENTIQUE PEUT SERVIR A UNE COMPARAISON MAIS PEUT AUSSI COMPLIQUE
            """

            try:
                with db.atomic():
                    self.user.name = name
                    self.user.email = email
                    self.user.password = password
                    self.user.role = role
                    self.user.salt = salt
                    self.user.save()
            except IntegrityError as e:
                raise ValueError(f"Erreur d'intégrité des données : {e}")
            return user



    """
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
        return user
