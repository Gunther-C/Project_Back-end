import click
from .controllers import Controllers



@click.command()
@click.option('--name', prompt="Name", required=True)
@click.option('--email', prompt="Email", required=True)
@click.option('--password', prompt="Password", required=True)
@click.option('--confirm-password', prompt="confirme password", required=True)
@click.option('--role', type=click.Choice(['commercial', 'gestion', 'support']), prompt="Rôle", required=True)
def create_user(name, email, password, confirm_password, role):
    try:
        user = Controllers().create(name, email, password, confirm_password, role)
        click.echo(f"Utilisateur {user.name} créé avec succès, Son rôle {user.role} !")
    except ValueError as e:
        click.echo(f"Erreur : {e}")

@click.command()
@click.option('--email', prompt="Email", required=True)
@click.option('--password', prompt="Password", required=True)
def login_user(email, password):
    if Controllers().login(email, password):
        """
        Redirection
        OU ET,
        Accès table avec bouton pour voir clients, contrats, événements (lecture seule).
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
