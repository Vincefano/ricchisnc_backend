from django.conf import settings
from django.core.exceptions import ValidationError
from oauth2_provider.management.commands.createapplication import (
    Command as CreateApplicationCommand,
)
from oauth2_provider.models import Application, get_application_model

OAuth2App = get_application_model()
OAUTH2_APP_NAME = settings.OAUTH2_APP_NAME


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
        kwargs["authorization_grant_type"] = "client-credentials"
        try:
            OAuth2App.objects.get(
                name=kwargs["name"],
                client_type=kwargs["client_type"],
                authorization_grant_type=kwargs["authorization_grant_type"],
            )
        except OAuth2App.DoesNotExist:
            application_fields = [field.name for field in Application._meta.fields]
            application_data = {}
            for key, value in kwargs.items():
                if key in application_fields and (isinstance(value, bool) or value):
                    if key == "user":
                        application_data.update({"user_id": value})
                    else:
                        application_data.update({key: value})

            new_application = Application(**application_data)

            try:
                new_application.full_clean()
            except ValidationError as exc:
                errors = "\n ".join(
                    [
                        "- " + err_key + ": " + str(err_value)
                        for err_key, err_value in exc.message_dict.items()
                    ]
                )
                self.stdout.write(
                    self.style.ERROR(
                        "Please correct the following errors:\n %s" % errors
                    )
                )
            else:
                cleartext_secret = new_application.client_secret
                new_application.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        "New application %s created successfully."
                        % new_application.name
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS("Client ID: %s" % new_application.client_id)
                )
                if "client_secret" not in application_data:
                    self.stdout.write(
                        self.style.SUCCESS("Client Secret: %s" % cleartext_secret)
                    )
