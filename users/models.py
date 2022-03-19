from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    #user_id = models.BigIntegerField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #created = models.DateField(auto_now_add=True)
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []


def __str__(self):
    return self.name
