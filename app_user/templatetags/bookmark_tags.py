# MainApp/templatetags/bookmark_tags.py
from django import template
from django.contrib.auth.models import User

from MainApp.models import Bookmark

register = template.Library()

@register.filter
def has_bookmark(post, user):
    return Bookmark.objects.filter(post=post, user=user).exists()