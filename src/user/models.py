from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # name = models.CharField(max_length=75)
    # company = models.CharField(max_length=75)
    # bio = models.TextField(max_length=500)
    # website = models.CharField(max_length=75)
    pass

    def __str__(self):
        return self.username