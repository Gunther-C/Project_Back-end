from core.config_peewee import db
from peewee import Model, AutoField, CharField, DateTimeField, ForeignKeyField
from passlib.hash import argon2
import datetime


class BaseModel(Model):
    class Meta:
        database = db


class Role(BaseModel):
    role = CharField(max_length=10, null=False)


class User(BaseModel):
    id = AutoField()
    name = CharField()
    email = CharField(unique=True, null=False)
    password = CharField(null=False)
    role = ForeignKeyField(Role, on_delete='CASCADE', backref='users')
    date = DateTimeField(default=datetime.datetime.now)

    def password_hash(self, new_password):
        self.password = aragon2.hash(new_password)

    def password_verif(self, verif_password):
        return argon2.verify(verif_password, self.password)
