from django import template
from pages.models import Message


register = template.Library()

@register.simple_tag
def count_unread_messages(to_user, from_user=None):
    unread_messages = Message.objects.filter(recipient=to_user, is_seen=False)
    if from_user:
        unread_messages = unread_messages.filter(sender=from_user)

    return unread_messages.count()
