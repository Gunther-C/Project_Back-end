import pytest
import datetime
from tests.conftest import bdd, contract_testing, customer_testing
from authentication.models import User
from customers.models import Customer, Contract


class TestContract:

    def test_contract_create(self, bdd, contract_testing):
        contract = contract_testing[0]
        new_date = contract_testing[1]
        assert contract.customer.name == "Customer"
        assert contract.seller.name == "Commercial 1"
        assert contract.total_invoice == 1000.0
        assert contract.outstanding == 200.0
        assert contract.created_date == new_date
        assert contract.status_sign

    def test_contract_update(self, bdd, contract_testing):
        contract = contract_testing[0]
        new_date = datetime.datetime.now()

        contract.seller = User.get(User.name == "Commercial 2")
        contract.total_invoice = 2000.0
        contract.outstanding = 400.0
        contract.created_date = new_date
        contract.status_sign = False
        contract.save()

        new_contract = Contract.get(Contract.id == contract.id)
        assert new_contract.seller.name == "Commercial 2"
        assert new_contract.total_invoice == 2000.0
        assert new_contract.outstanding == 400.0
        assert new_contract.created_date == new_date
        assert not new_contract.status_sign

    def test_contract_delete(self, bdd, contract_testing):
        contract = contract_testing[0]
        contract.delete_instance()
        assert not Contract.select().where(Contract.id == contract.id).exists()

