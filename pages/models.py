from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.conf.global_settings import LANGUAGES


GENDERS = [
    ("M", "Male"),
    ("F", "Female"),
]


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique = True)
    age = models.SmallIntegerField(default=0, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    country = CountryField()
    native_language = models.CharField(max_length=8, choices=LANGUAGES, blank=True, null=True)
    practising_language = models.CharField(max_length=8, choices=LANGUAGES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images", default="default-profile-picture.jpg")
    is_online = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username