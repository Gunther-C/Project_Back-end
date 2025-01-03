from core.config_peewee import db
from authentication.models import User
from customers.models import Customer, Contract
from peewee import Model, AutoField, DateTimeField, ForeignKeyField
from peewee import BooleanField, CharField, TextField, IntegerField, FloatField
import datetime


class Event(Model):
    id = AutoField()
    contract = ForeignKeyField(Contract, on_delete='CASCADE', backref='events')
    customer = ForeignKeyField(Customer, on_delete='CASCADE', backref='events')
    support = ForeignKeyField(User, on_delete='CASCADE', backref='events')
    event_start = DateTimeField(default=datetime.datetime.now)
    event_finish = DateTimeField(null=True)
    location = CharField(null=False)
    attendees = IntegerField(default=0)
    note = TextField(null=True)

    class Meta:
        database = db

    def event_end(self):
        self.event_finish = datetime.datetime.now()
