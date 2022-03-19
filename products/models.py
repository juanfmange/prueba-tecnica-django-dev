from django.db import models
from users.models import User
# Create your models here.

class Products(models.Model):
    product = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)



