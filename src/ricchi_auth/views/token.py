import hashlib
import json
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from oauth2_provider.views.base import TokenView

AccessToken = get_access_token_model()


class CustomTokenView(TokenView):

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        url, headers, body, status = self.create_token_response(request)
        body = json.loads(body)
        if status == 200:
            access_token = body.get("access_token")
            if access_token is not None:
                token_checksum = hashlib.sha256(
                    access_token.encode("utf-8")
                ).hexdigest()
                token = get_access_token_model().objects.get(
                    token_checksum=token_checksum
                )
                app_authorized.send(sender=self, request=request, token=token)
                access_token_obj = AccessToken.objects.get(token=token)
                body["expires"] = str(access_token_obj.expires)
                del body["expires_in"]
        response = HttpResponse(content=json.dumps(body), status=status)

        for k, v in headers.items():
            response[k] = v
        return response
