from core.config_tables import CreateTable, ViewTable
from core.config_keys import encryption_key, jwt_key
from core.config_sentry import conf_sentry
from core.config_keys import encryption_key

from authentication.models import User
from customers.models import Customer, Contract
from events.models import Event

from authentication.views import create_user, login_user





if __name__ == "__main__":
    # create_user()
    login_user()

    # conf_sentry()

    # CreateTable(User)
    # ViewTable(User)

    # jwt_key()
    # encryption_key('PASSWORD_KEY')

    """
    Créer un user (admin) qui puisse avoir access a la bdd
    
    Comment modifier la couleur (entre autre des messages d'alerte)
     
    Mettre rich en place pour les tables
    
    Mettre en place les permissions (dans le token ?)
    
    Ajouter des cryptages au controller du customer (déplacer du model au controller)
    """
