from django.http.response import HttpResponse
from oauth2_provider.views.generic import ProtectedResourceView


class AuthTestView(ProtectedResourceView):

    def get(self, request):
        return HttpResponse()
