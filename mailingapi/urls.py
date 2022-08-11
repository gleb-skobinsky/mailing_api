"""mailingapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from multiprocessing.connection import Client
from django.contrib import admin
from django.urls import path
from rest_framework.schemas import get_schema_view
from mailing.views import ClientApiView, MailingApiView
from django.views.generic import TemplateView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/mailing/", MailingApiView.as_view()),
    path("api/v1/client/", ClientApiView.as_view()),
    path("api/v1/client/<int:pk>/", ClientApiView.as_view()),
    path("api/v1/mailing/<int:pk>/", MailingApiView.as_view()),
]

urlpatterns += doc_urls
