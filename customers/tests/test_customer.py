import pytest
import datetime
from tests.conftest import bdd, customer_testing
from authentication.models import User
from customers.models import Customer


class TestCustomer:

    def test_customer_create(self, bdd, customer_testing):
        customer = customer_testing[0]
        new_date = customer_testing[1]
        assert customer.detail == "Detail customer"
        assert customer.name == "Customer"
        assert customer.email == "customer@f.fr"
        assert customer.phone == "+33 6 07 08 09 10"
        assert customer.business_name == "Business name"
        assert customer.update_date == new_date
        assert customer.seller.id == 1

    def test_update_customer(self, bdd, customer_testing):
        customer = customer_testing[0]
        new_date = datetime.datetime.now()

        customer.detail = "New Detail customer"
        customer.name = "New Customer"
        customer.email = "newcustomer@f.fr"
        customer.phone = "+33 6 07 08 09 11"
        customer.business_name = "New Business name"
        customer.seller = User.get(User.name == "Commercial 2")
        customer.update_date = new_date
        customer.save()

        new_customer_testing = Customer.get(Customer.id == customer.id)
        assert new_customer_testing.detail == "New Detail customer"
        assert new_customer_testing.name == "New Customer"
        assert new_customer_testing.email == "newcustomer@f.fr"
        assert new_customer_testing.phone == "+33 6 07 08 09 11"
        assert new_customer_testing.business_name == "New Business name"
        assert new_customer_testing.business_name == "New Business name"
        assert new_customer_testing.update_date == new_date

    def test_delete_customer(self, bdd, customer_testing):
        customer = customer_testing[0]
        customer.delete_instance()
        assert not Customer.select().where(Customer.id == customer.id).exists()
