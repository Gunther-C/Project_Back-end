from core.config_peewee import db
from core.config_sentry import conf_sentry
from core.config_keys import encryption_key
from authentication.models import User, Salt
from customers.models import Customer, Contract
from events.models import Event

from authentication.views import create_user


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
    create_user()

    # conf_sentry()
    # CreateTable(User)
    """
    key = encryption_key()
    print(key)
    """
