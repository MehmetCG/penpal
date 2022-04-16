from urllib import request
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.generics import ListCreateAPIView
from .serializers import UserSerializer
from django.conf.global_settings import LANGUAGES
from django_countries import countries
from.models import User

class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["languages"] = LANGUAGES
       context["countries"] = countries
       return context

class ProfileDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = "login"
    template_name = "profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(
            object=self.object, languages=LANGUAGES, countries=countries
        )
        return self.render_to_response(context)

    def has_permission(self):
        return self.request.user == self.get_object()


class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    
    def get_queryset(self):
        self.queryset = User.objects.exclude(username=self.request.user)
        return super().get_queryset()
    