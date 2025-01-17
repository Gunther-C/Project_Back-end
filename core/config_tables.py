from .config_peewee import db
from authentication.models import User, Salt
from customers.models import Customer, Contract
from events.models import Event

from cryptography.fernet import Fernet


class CreateTable:
    def __init__(self, model):
        self.db = db
        self.model = model
        self.db.connect()

        self.create_table()

    def create_table(self):
        db.create_tables([self.model])
        self.db.close()
        ViewTable(self.model)


class ViewTable:
    def __init__(self, model):
        self.db = db
        self.model = model
        self.db.connect()

        self.show_table_config()

    def show_table_config(self):

        columns = self.db.execute_sql(f"PRAGMA table_info({self.model._meta.table_name});").fetchall()
        self.db.close()

        for column in columns:
            column_id = column[0]
            column_name = column[1]
            column_type = column[2]
            not_null = "NOT NULL" if column[3] else "NULL"
            default_value = column[4]
            primary_key = "PRIMARY KEY" if column[5] else ""

            print(f"ID: {column_id}, Nom: {column_name}, Type: {column_type}, {not_null}, Default: {default_value}, {primary_key}")




