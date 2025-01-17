import os
import secrets
from dotenv import load_dotenv
from cryptography.fernet import Fernet


def jwt_key():
    secret_key = secrets.token_urlsafe(64)
    with open('.env', 'a') as f:
        f.write(f"\nSECRET_KEY={secret_key}")


def encryption_key(name_key):
    key = Fernet.generate_key()
    with open('.env', 'a') as f:
        f.write(f"\n{name_key}={key.decode()}")

