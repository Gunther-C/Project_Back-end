import click
from core.config_peewee import db
from .controllers import Controllers
import peewee


@click.command()
@click.option('--name', prompt="Name", help="Nom de l'utilisateur")
@click.option('--email', prompt="Email", help="Email de l'utilisateur")
@click.option('--password', prompt="Password", help="Mot de passe de l'utilisateur")
@click.option('--confirm-password', prompt="confirme password", help="Confirmez le mot de passe")
@click.option('--role', type=click.Choice(['commercial', 'gestion', 'support']), prompt="Rôle",
              help="Rôle de l'utilisateur")
def create_user(name, email, password, confirm_password, role):
    try:
        user = Controllers().create(name=name, email=email, password=password, confirm_password=confirm_password,
                                  role=role)
        click.echo(f"Utilisateur {user.name} créé avec succès !")
        click.echo(f"Son rôle {user.role} créé avec succès !")
    except ValueError as e:
        click.echo(f"Erreur : {e}")

@click.command()
@click.option('--email', prompt="Email", help="Email de l'utilisateur")
@click.option('--password', prompt="Password", help="Mot de passe de l'utilisateur")
def login_user(email, password):
    try:
        user = User.get(User.email == email)
        if Controllers().verify_password(user, password):
            """
            Création du token
            """
            click.echo(f"Connexion réussie!")

        else:
            click.echo("Mot de passe incorrect.")
    except peewee.DoesNotExist:
        click.echo("Utilisateur non trouvé.")
    except Exception as e:
        click.echo(f"Erreur lors de la connexion : {e}")

