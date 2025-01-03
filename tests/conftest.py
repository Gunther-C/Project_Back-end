import pytest
from peewee import SqliteDatabase
from passlib.hash import argon2
import datetime
from authentication.models import Role, User
from customers.models import Customer, Contract
from events.models import Event

db = SqliteDatabase(':memory:')


@pytest.fixture
def bdd():
    db.bind([Role, User, Customer, Contract, Event])
    db.connect()
    db.create_tables([Role, User, Customer, Contract, Event])

    yield
    db.drop_tables([Role, User, Customer, Contract, Event])
    db.close()


@pytest.fixture
def user_testing(bdd):
    role = Role.create(role="support")
    password = argon2.hash("password")
    user = User.create(name="Gunther", email="gunther@email.com", password=password, role=role)

    yield user
    role.delete_instance()
    user.delete_instance()


@pytest.fixture
def customer_testing(bdd):
    User.insert_many(
        [
            {"name": "Commercial 1", "email": "commercial1@f.fr", "password": "password", "role": "commercial"},
            {"name": "Commercial 2", "email": "commercial2@f.fr", "password": "password", "role": "commercial"}
        ]
    ).execute()
    commercial = User.get(User.name == "Commercial 1")
    new_date = datetime.datetime.now()
    customer = Customer.create(
        detail="Detail customer",
        name="Customer",
        email="customer@f.fr",
        phone="+33 6 07 08 09 10",
        business_name="Business name",
        created_date=new_date,
        update_date=new_date,
        seller=commercial.id
    )
    yield customer, new_date
    customer.delete_instance()
    User.truncate_table()


@pytest.fixture
def contract_testing(bdd, customer_testing):
    _customer = customer_testing[0]
    new_date = customer_testing[1]
    contract = Contract.create(
        customer=_customer,
        seller=_customer.seller,
        total_invoice=1000.0,
        outstanding=200.0,
        created_date=new_date,
        status_sign=True
    )
    yield contract, new_date
    contract.delete_instance()


@pytest.fixture
def event_testing(bdd, contract_testing, user_testing):
    _contract = contract_testing[0]
    new_date = datetime.datetime.now()
    event = Event.create(
        contract=_contract,
        customer=_contract.customer,
        support=user_testing,
        event_start=new_date,
        event_finish="null",
        location="Rue du Nouveau Évènement",
        attendees=10,
        note="Nouveau Évènement"
    )
    yield event, new_date
    event.delete_instance()
