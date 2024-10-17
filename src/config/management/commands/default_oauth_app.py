from django.conf import settings
from django.core.exceptions import ValidationError
from oauth2_provider.management.commands.createapplication import (
    Command as CreateApplicationCommand,
)
from oauth2_provider.models import Application, get_application_model

OAuth2App = get_application_model()


class Command(CreateApplicationCommand):
    help = "Crea una nuova applicazione OAuth"

    def add_arguments(self, parser):
        parser.add_argument(
            "--client_type", type=str, nargs="?", default="confidential"
        )
        parser.add_argument("--authorization_grant_type", nargs="?", default="password")

    def handle(self, *args, **kwargs):
        kwargs["name"] = settings.OAUTH2_APP_NAME
        kwargs["client_type"] = "confidential"
        kwargs["authorization_grant_type"] = "password"
        try:
            OAuth2App.objects.get(
                name=kwargs["name"],
                client_type=kwargs["client_type"],
                authorization_grant_type=kwargs["authorization_grant_type"],
            )
        except OAuth2App.DoesNotExist:
            print("SAVE THESE CREDENTIALS! THEY WON'T BE SHOWED AGAIN!")
            super().handle(*args, **kwargs)
            oauth_app = OAuth2App.objects.get(
                name=kwargs["name"],
                client_type=kwargs["client_type"],
                authorization_grant_type=kwargs["authorization_grant_type"],
            )
            print(f"Client ID: {oauth_app.client_id}")
