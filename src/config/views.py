from django.http.response import HttpResponse
from django.views import View


class Healthz(View):
    """Health check endpoint"""

    def get(self, request):
        return HttpResponse()
