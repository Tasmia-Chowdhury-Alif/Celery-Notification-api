from django.contrib.auth.models import AbstractUser
from django.db import models

from users.managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  # email as username field
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email