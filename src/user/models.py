from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _

class CustomUser(AbstractUser):
    name = models.CharField(max_length=75)
    company = models.CharField(max_length=75)
    position = models.CharField(max_length=75)
    bio = models.TextField(max_length=500)
    website = models.CharField(max_length=75)
    twitter = models.CharField(max_length=75)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()
    def __str__(self):
        return self.username