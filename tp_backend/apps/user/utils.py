import os

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

from .models import User


def getAccount(userUuid):
    try:
        return User.objects.get(uuid=userUuid)
    except:
        return None