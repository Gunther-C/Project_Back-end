
from core.config_peewee import db
from authentication.models import User
from peewee import Model, AutoField, BooleanField, CharField, TextField, FloatField, DateTimeField, ForeignKeyField
import uuid
import datetime


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

    def new_date(self):
        self.update_date = datetime.datetime.now()


class Contract(BaseModel):
    id = CharField(primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, null=False)
    customer = ForeignKeyField(Customer, on_delete='CASCADE', backref='contracts')
    seller = ForeignKeyField(User, on_delete='CASCADE', backref='contracts')
    total_invoice = FloatField(null=False)
    outstanding = FloatField(default=0.0)
    created_date = DateTimeField(default=datetime.datetime.now)
    status_sign = BooleanField(default=False)
