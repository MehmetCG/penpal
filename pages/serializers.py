from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    country = serializers.CharField(source='get_country_display')
    native_language = serializers.CharField(source='get_native_language_display')
    practising_language = serializers.CharField(source='get_practising_language_display')
    last_login = serializers.SerializerMethodField()

    def get_last_login(self, obj):
        return obj.last_login.strftime("%H:%M, %d %B %Y")
    
    class Meta:
            model = User
            fields = '__all__'