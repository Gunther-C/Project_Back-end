import uuid
import datetime
from core.config_peewee import db
from peewee import Model, AutoField, UUIDField, CharField, DateTimeField, ForeignKeyField


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
