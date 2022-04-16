from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from django.conf.global_settings import LANGUAGES


GENDERS = [
    ("M", "Male"),
    ("F", "Female"),
]


User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.SmallIntegerField(default=0, blank=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    country = CountryField(blank_label='(Select Country)', blank=True, null=True)
    native_language = models.CharField(max_length=8, choices=LANGUAGES, blank=True, null=True)
    practising_language = models.CharField(max_length=8, choices=LANGUAGES, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="images", default="default-profile-picture.jpg")
    is_online = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)