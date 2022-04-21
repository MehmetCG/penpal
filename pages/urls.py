from re import template
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path(
        "login/", 
        LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), 
        name="login"
    ),
    path("logout/", LogoutView.as_view(template_name="login.html"), name="logout"),
    path("", HomeView.as_view(), name="home" ),
    path("profile/<username>/", ProfileDetailView.as_view(), name="profile"),
    path("chat/<to_user>/", ChatView.as_view(), name="chat"),
]