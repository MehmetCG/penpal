from webbrowser import get
from rest_framework import serializers
from .models import User, Profile


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
            model = User
            fields = ("username", "email", "password")


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    def get_last_login(self, obj):
        return obj.last_login.strftime("%H:%M, %d %B %Y")
    class Meta:
        model = Profile
        fields = "__all__"