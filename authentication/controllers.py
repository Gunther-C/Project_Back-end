import os
import validators
from core.config_peewee import db
from authentication.models import User, Salt
from passlib.hash import argon2
from dotenv import load_dotenv
from cryptography.fernet import Fernet


load_dotenv()

key_password = os.getenv('PASSWORD_KEY').encode()
fernet_password = Fernet(key_password)

key_email = os.getenv('EMAIL_KEY').encode()
fernet_email = Fernet(key_email)

key_role = os.getenv('ROLE_KEY').encode()
fernet_role = Fernet(key_role)


def control_user(name, email, password, confirm_password, role):
    if password != confirm_password:
        raise ValueError("Les mots de passe ne correspondent pas")

    if not validators.email(email):
        raise ValueError("Email invalid")

    encrypted_email = fernet_email.encrypt(email.encode()).decode()
    encrypted_role = fernet_role.encrypt(role.encode()).decode()

    new_salt = os.urandom(16).hex()
    salt = Salt.create(salt=new_salt)
    encrypted_password = argon2.hash(key_password + password.encode() + salt.salt.encode())

    with db.atomic():
        user = User.create(name=name, email=encrypted_email, password=encrypted_password,
                           role=encrypted_role, salt=salt)
        user.save()
    return user


def verify_password(user, verif_password):
    return argon2.verify(key_password + verif_password.encode() + user.salt.salt.encode(), user.password)


def decrypt_email(user):
    return fernet_email.decrypt(user.email.encode()).decode()


def decrypt_role(user):
    return fernet_role.decrypt(user.role.encode()).decode()
