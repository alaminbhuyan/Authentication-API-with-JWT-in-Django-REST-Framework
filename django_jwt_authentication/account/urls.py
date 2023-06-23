from django.urls import path
from account.views import *
urlpatterns = [
    path(route="", view=home, name="home"),
]


