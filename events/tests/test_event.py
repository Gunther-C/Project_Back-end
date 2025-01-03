import pytest
import datetime
from tests.conftest import bdd, event_testing, contract_testing, customer_testing, user_testing
from authentication.models import User
from events.models import Event


class TestEvent:

    def test_event_create(self, bdd, event_testing):
        event = event_testing[0]
        new_date = event_testing[1]
        assert event.customer.name == "Customer"
        assert event.support.name == "Gunther"
        assert event.event_start == new_date
        assert event.event_finish == "null"
        assert event.location == "Rue du Nouveau Évènement"
        assert event.attendees == 10
        assert event.note == "Nouveau Évènement"

    def test_event_update(self, bdd, event_testing):
        event = event_testing[0]
        new_date = datetime.datetime.now()

        event.support = User.get(User.name == "Commercial 2")
        event.event_finish = new_date
        event.location = "Bd du Nouveau Évènement"
        event.attendees = 20
        event.note = "Nouveau Évènement du sud"
        event.save()

        new_event = Event.get(Event.id == event.id)
        assert new_event.support.name == "Commercial 2"
        assert new_event.event_finish == new_date
        assert new_event.location == "Bd du Nouveau Évènement"
        assert new_event.attendees == 20
        assert new_event.note == "Nouveau Évènement du sud"

    def test_event_delete(self, bdd, event_testing):
        event = event_testing[0]
        event.delete_instance()
        assert not Event.select().where(Event.id == event.id).exists()
