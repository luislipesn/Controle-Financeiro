from django.urls import path
from django.contrib.auth.views import LoginView

from accounts import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
