from django.db import models
from django.contrib.auth.models import AbstractUser

# Implementing a custom user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True,null=False)
    username = models.CharField(max_length=50, unique=True,default=None)

    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
