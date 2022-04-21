from django.urls import path
from .views import *


urlpatterns = [
    path("user_create/", UserCreateView.as_view(), name="user-create"),
    path("profile_list/", ProfileListView.as_view(), name="profile-list"),
    path("profile_update/<username>/", ProfileUpdateView.as_view(), name="profile-update"),
]