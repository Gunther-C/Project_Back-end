import uuid
import datetime
from core.config_peewee import db
from peewee import Model, UUIDField, CharField, DateTimeField


class User(Model):
    CHOICES = [("commercial", "Commercial"), ("gestion", "Gestion"), ("support", "Support")]

    id = UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = CharField(null=False)
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    role = CharField(choices=CHOICES, null=False)
    date = DateTimeField(default=datetime.datetime.now)
    salt = CharField(null=False)

    class Meta:
        database = db
