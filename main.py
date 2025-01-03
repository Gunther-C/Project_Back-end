from core.config_peewee import db
from authentication.models import User, Role
from customers.models import Customer, Contract
from events.models import Event


class CreateTable:
    def __init__(self, model):
        self.db = db
        self.model = model
        self.db.connect()

        self.create_table()

    def create_table(self):
        db.create_tables([self.model])
        self.show_table_config()

    def show_table_config(self):
        columns = self.db.execute_sql(f"PRAGMA table_info({self.model._meta.table_name});").fetchall()
        self.db.close()

        for column in columns:
            print(f"{column[1]}, Type: {column[2]}")


if __name__ == "__main__":
    CreateTable(Event)
