from django.urls import path
from account.views import *


urlpatterns = [
    path(route="register/", view=UserRegistrationView.as_view(), name="register"),
]


