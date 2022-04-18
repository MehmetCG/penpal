from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
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

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(user_logged_in)
def make_online(sender, user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()

@receiver(user_logged_out)
def make_offline(sender, user, request, **kwargs):
    try:
        user.profile.is_online = False
        user.profile.save()
    except:
        # user is None if it was not authenticated
        pass