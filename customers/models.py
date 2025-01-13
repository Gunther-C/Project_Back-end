import os
import uuid
import datetime
import validators
from core.config_peewee import db
from authentication.models import User
from peewee import Model
from peewee import AutoField, UUIDField, BooleanField, CharField, TextField, FloatField, DateTimeField, ForeignKeyField
from dotenv import load_dotenv
from cryptography.fernet import Fernet


load_dotenv()
key_phone = os.getenv('PHONE_KEY').encode()
fernet_phone = Fernet(key_phone)


class BaseModel(Model):
    class Meta:
        database = db


class Customer(BaseModel):
    id = AutoField()
    detail = TextField(null=True)
    name = CharField(null=False)
    email = CharField(unique=True, null=False)
    phone = CharField(unique=True, null=False)
    business_name = CharField(null=False)
    created_date = DateTimeField(default=datetime.datetime.now)
    update_date = DateTimeField(default=datetime.datetime.now)
    seller = ForeignKeyField(User, on_delete='CASCADE', backref='customers')

    def save(self, *args, **kwargs):
        if self.email:
            if not validators.email(self.email):
                raise ValueError("Email invalid")
            self.email = fernet_email.encrypt(self.email.encode()).decode()

        if self.phone:
            if not validators.phone(self.phone):
                raise valueError("Le numéro de téléphone n'est pas valide")
            self.phone = fernet_phone.encrypt(self.phone.encode()).decode()

        super(Customer, self).save(*args, **kwargs)

    def new_date(self):
        self.update_date = datetime.datetime.now()


class Contract(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    customer = ForeignKeyField(Customer, on_delete='CASCADE', backref='contracts')
    seller = ForeignKeyField(User, on_delete='CASCADE', backref='contracts')
    total_invoice = FloatField(null=False)
    outstanding = FloatField(default=0.0)
    created_date = DateTimeField(default=datetime.datetime.now)
    status_sign = BooleanField(default=False)
