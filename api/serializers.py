from rest_framework import serializers
from pages.models import User, Profile, Message


class UserSerializer(serializers.ModelSerializer): 
    class Meta:
            model = User
            fields = ("username", "email", "password")


class ProfileReadSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    gender = serializers.CharField(source='get_gender_display')
    country = serializers.CharField(source='get_country_display')
    native_language = serializers.CharField(source='get_native_language_display')
    practising_language = serializers.CharField(source='get_practising_language_display')

    def get_username(self, obj):
        return obj.user.username

    def get_last_login(self, obj):
        last_login = obj.user.last_login or obj.user.date_joined
        return last_login.strftime("%H:%M, %d %B %Y")
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ("image",)


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = "__all__"