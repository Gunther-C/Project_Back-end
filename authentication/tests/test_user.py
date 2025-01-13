import pytest
from passlib.hash import argon2
from tests.conftest import bdd, user_testing
from authentication.models import User


class TestUser:

    def test_create_user(self, bdd, user_testing):
        assert user_testing.name == "Gunther"
        assert user_testing.email == "gunther@email.com"
        assert argon2.verify("password", user_testing.password)
        assert user_testing.role.role == "support"

    def test_update_user(self, bdd, user_testing):
        user_testing.name = "Douglas"
        user_testing.email = "douglas@email.com"
        user_testing.password = argon2.hash("new_password")
        user_testing.role = "admin"
        user_testing.save()

        new_user_testing = User.get(User.id == user_testing.id)
        assert new_user_testing.name == "Douglas"
        assert new_user_testing.email == "douglas@email.com"
        assert argon2.verify("new_password", user_testing.password)
        assert new_user_testing.role == "admin"

    def test_delete_user(self, user_testing):
        user_testing.delete_instance(recursive=True)
        assert not User.select().where(User.id == user_testing.id).exists()
