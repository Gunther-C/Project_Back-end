import click
from core.config_peewee import db
from .controllers import control_user, verify_password, decrypt_email, decrypt_role
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
        user = control_user(name, email, password, confirm_password, role)
        click.echo(f"Utilisateur {user.name} créé avec succès !")
        click.echo(f"Son rôle {decrypt_role(user)} créé avec succès !")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
