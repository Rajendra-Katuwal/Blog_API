from django.db import models
from django.contrib.auth.models import AbstractUser

# Implementing a custom user model
# class CustomUser(AbstractUser):
#     email = models.EmailField()
#     username = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     bio = models.TextField(null=True, blank=True)
#     date_joined = models.DateField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)
