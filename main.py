from core.config_tables import CreateTable, ViewTable
from core.config_keys import encryption_key, jwt_key
from core.config_sentry import conf_sentry
from core.config_keys import encryption_key

from authentication.models import User
from customers.models import Customer, Contract
from events.models import Event

from authentication.views import create_user, login_user, update_user
from authentication.auth import AuthManager





if __name__ == "__main__":
    # create_user()
    # login_user()
    update_user()

    # conf_sentry()

    # AuthManager().token_delete()
    # AuthManager().token_get()

    # CreateTable(User)
    # ViewTable(User)

    # jwt_key()
    # encryption_key('PASSWORD_KEY')
