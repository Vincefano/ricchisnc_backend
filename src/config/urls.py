"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, re_path
from oauth2_provider import urls
from oauth2_provider import views as oauth2_views

from ricchi_auth.views.test import AuthTestView
from ricchi_auth.views.token import CustomTokenView

from .views import Healthz

oauth2_patters = (
    [
        # Base urls
        path("oauth/token/", CustomTokenView.as_view(), name="token"),
        path(
            "oauth/revoke_token/",
            oauth2_views.RevokeTokenView.as_view(),
            name="revoke-token",
        ),
    ]
    + urls.management_urlpatterns
    + urls.oidc_urlpatterns
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test/", AuthTestView.as_view(), name="test"),
    path("healthz/", Healthz.as_view(), name="healthz"),
] + oauth2_patters
