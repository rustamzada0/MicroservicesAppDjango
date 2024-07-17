from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email