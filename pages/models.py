from pyexpat import model
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

def get_deleted_user():
    deleted_user, _ = User.objects.get_or_create(username="Deleted")
    return deleted_user


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


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name="sender")
    recipient = models.ForeignKey(User, on_delete=models.SET(get_deleted_user), related_name= "recipient")
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add= True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class LatestMessage(models.Model):
    senders = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=True, null=True)


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

@receiver(post_save, sender=Message)
def set_latest(sender, instance, created, **kwargs):
    m_sender= instance.sender
    m_recipient = instance.recipient
    text = instance.text
    obj = LatestMessage.objects.filter(senders=m_sender).filter(senders=m_recipient)
    if obj:
        obj.update(text=text)
    else:
        LatestMessage.objects.create(text=text).senders.add(m_sender, m_recipient)