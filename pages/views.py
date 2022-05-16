from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf.global_settings import LANGUAGES
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_countries import countries
from .models import Profile, User, Message


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
    slug_field = "user__username"
    slug_url_kwarg = "username"
    model = Profile

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(
            object=self.object, languages=LANGUAGES, countries=countries
        )
        return self.render_to_response(context)

    def has_permission(self):
        return self.request.user == self.get_object().user


class ChatView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "chat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        path = self.kwargs.get("to_user_id")
        latest_messages = user.latestmessage_set.all().order_by("-created_at")
        context["latest_messages"] = latest_messages  
        
        to_user = None
        if path != "inbox":
            to_user = get_object_or_404(User, id=path)
            messages = Message.objects.filter(Q(
                Q(sender=user) & Q(recipient=to_user)) \
                | (Q(sender=to_user) & Q(recipient=user)
            ))
            context["messages"] = messages
            Message.read_all(to_user, user)
        context["to_user"] = to_user

        return context
