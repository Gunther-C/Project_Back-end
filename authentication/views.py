import click
from .controllers import Controllers
from .permissions import Permissions

permissions = Permissions()
is_authenticated = permissions.is_authenticated()


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


@click.command()
def update_user():
    if is_authenticated is None:
        click.echo("Vous n'êtes pas autorisé!")
        return

    user = permissions.user

    """
        ATTENTION permissions.user VA ETRE DIFFERENT DE controller.user
        DECONNEXION ET RECONNEXION NECESSAIRE OU AUTRE
        AVANCER AVEC DEUX OBJECT USER IDENTIQUE PEUT SERVIR A UNE COMPARAISON MAIS PEUT AUSSI COMPLIQUE
    """
    name = click.prompt("Name", type=str, default=user.name)
    email = click.prompt("Email", type=str, default=user.email)
    password = click.prompt("Password", type=str, default='')
    confirm_password = click.prompt("Confirm password", default='')
    role = click.prompt("Role", type=click.Choice(['commercial', 'gestion', 'support']), default=user.role)

    if Controllers().update(name, email, password, confirm_password, role):
        click.echo(f"Modification(s) sauvegardée(s)!")


@click.command()
def login_user():
    if is_authenticated:
        click.echo("Vous êtes déjà connecté.")
        return

    email = click.prompt("Email", type=str)
    password = click.prompt("Password", type=str)

    if not email or not password:
        click.echo("Tous les champs sont obligatoires.")
        return

    if Controllers().login(email, password):
        click.echo(f"Connexion réussie!")
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
