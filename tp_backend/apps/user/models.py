import random
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .constants import Roles


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    updatedAt = models.DateTimeField(blank=True, null=True, auto_now=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        # This makes the model abstract, so it won’t create a database table
        abstract = True



class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=64, blank=True)

    isActive = models.BooleanField(default=True)
    verificationEmailSentAt = models.DateTimeField(blank=True, null=True)
    verificationCode = models.CharField(max_length=6, null=True, blank=True)

    role = models.CharField(
        max_length=64,
        choices=Roles.choices,
        default=Roles.GUEST,
    )


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = 'user'

    def __str__(self):
        return "[{pk}] {email}".format(pk=self.pk, email=self.email)
    
    @property
    def is_authenticated(self):
        return True

    def generateVerificationCode(self):
        verifyCode = ""
        for i in range(1, 7):
            verifyCode += str(random.randint(0, 9))
        self.verificationCode = verifyCode
        self.save()


def createSuperuser(email, password):
    user = User.objects.create(
        email=email,
        is_staff=True,
        isActive=True,
        is_superuser=True,
    )
    user.set_password(password)
    user.save()
    return user

def deleteUser(email):
    user = User.objects.filter(email__iexact=email, deletedAt__isnull=True).first()
    if not user:
        return False
    user.deletedAt = models.DateTimeField(auto_now=True)
    user.isActive = False
    user.save()
    return True


""" @receiver(pre_save, sender=User)
def ResetUserTokenWhenImportantFieldsChanges(sender, instance: User, **kwargs):
    if not instance.pk:
        return

    oldUser = User.objects.filter(pk=instance.pk).first()
    if not oldUser:
        return

    token = Token.objects.filter(user=instance).first()
    shouldResetToken = False
    if oldUser.isActive != instance.isActive:
        shouldResetToken = True

    if oldUser.role != instance.role:
        shouldResetToken = True

    if oldUser.email != instance.email:
        shouldResetToken = True

    if oldUser.password != instance.password:
        shouldResetToken = True

    if shouldResetToken:
        if token:
            token.delete()
            Token.objects.create(user=instance) """