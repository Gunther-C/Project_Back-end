import os
import uuid
import datetime
import validators
from core.config_peewee import db
from peewee import Model, AutoField, UUIDField, CharField, DateTimeField, ForeignKeyField
from passlib.hash import argon2
from dotenv import load_dotenv
from cryptography.fernet import Fernet


load_dotenv()

key_password = os.getenv('PASSWORD_KEY')
fernet_password = Fernet(key_password)

key_email = os.getenv('EMAIL_KEY').encode()
fernet_email = Fernet(key_email)

key_role = os.getenv('ROLE_KEY').encode()
fernet_role = Fernet(key_role)


class Salt(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    salt = CharField(unique=True, null=False)

    class Meta:
        database = db


class User(Model):
    CHOICES = [("commercial", "Commercial"), ("gestion", "Gestion"), ("support", "Support")]

    id = UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = CharField()
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    role = CharField(choices=CHOICES)
    date = DateTimeField(default=datetime.datetime.now)
    salt = ForeignKeyField(Salt, on_delete="CASCADE", backref="users", null=False)

    class Meta:
        database = db

    def save(self, *args, **kwargs):

        if self.password:
            new_salt = os.urandom(16).hex()
            self.salt = Salt.create(salt=new_salt)
            self.password = argon2.hash(key_password + self.password + self.salt.salt)

        if self.email:
            if not validators.email(self.email):
                raise ValueError("Email invalid")
            self.email = fernet_email.encrypt(self.email.encode()).decode()

        if self.role:
            self.role = fernet_role.encrypt(self.role.encode()).decode()

        super(User, self).save(*args, **kwargs)

    def password_verif(self, verif_password):
        return argon2.verify(key_password + verif_password + self.salt.salt, self.password)

    def decrypt_email(self):
        self.email = fernet_email.decrypt(self.email.encode()).decode()

    def decrypt_role(self):
        self.role = fernet_role.decrypt(self.role.encode()).decode()


