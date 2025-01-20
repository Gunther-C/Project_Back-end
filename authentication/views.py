import click
from .controllers import Controllers
from .permissions import Permissions

permissions = Permissions()

@click.command()
@click.option('--name', prompt="Name", type=str, required=True)
@click.option('--email', prompt="Email", type=str, required=True)
@click.option('--password', prompt="Password", type=str, required=True)
@click.option('--confirm-password', prompt="Confirme password", type=str, required=True)
@click.option('--role', type=click.Choice(['commercial', 'gestion', 'support']), prompt="Rôle", required=True)
def create_user(name, email, password, confirm_password, role):
    try:
        user = Controllers().create(name, email, password, confirm_password, role)
        click.echo(f"Utilisateur {user.name} créé avec succès, Son rôle {user.role} !")
        login_user()
    except ValueError as e:
        click.echo(f"Erreur : {e}")



""" default=user.name ect """
@click.command()
@click.option('--name', prompt="Name")
@click.option('--email', prompt="Email", required=True)
@click.option('--password', prompt="Password", required=True)
@click.option('--confirm-password', prompt="Confirme password", required=True)
@click.option('--role', type=click.Choice(['commercial', 'gestion', 'support']), prompt="Rôle", required=True)
def update_user(name, email, password, confirm_password, role):
    if Controllers().update(name, email, password, confirm_password, role):
        click.echo(f"Modification(s) sauvegardée(s)!")


@click.command()
def login_user():
    if permissions.is_authenticated():
        click.echo("Vous êtes déjà connecté.")
        return

    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str)

    if not email or not password:
        click.echo("Tous les champs sont obligatoires.")
        return

    if Controllers().login(email, password):
        """
        Accès pour voir clients, contrats, événements (lecture seule).
        De plus selon le rôle:
            Commercial => 
            - Création ou modification d'un compte client lui appartenant
            - Ses contrats et événements liés, 
            - Si le contrat est signé, création de l'événement (hors support)
            
            Gestion => 
            - Création et signature d'un contrat et association de ce contrat au client
            - Désigne un support une fois un événement créé
            
            Support =>
            - Ses événements
            - Modification / Mise à jour de ses événements
        """
