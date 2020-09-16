from django.db import models
from django.contrib.auth.models import AbstractUser

# Consider creating a custom user model from scratch as detailed at
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#specifying-a-custom-user-model


class User(AbstractUser):
    pass



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_name = models.CharField(max_length=25, null=False, blank=False, unique=True)
    profile_picture = models.ImageField(upload_to=None, height_field=None, width_field=None)
    description = models.TextField(null=True, blank=True)
    date_profile_updated = models.DateField(auto_now=True)
    date_created = models.DateField(auto_now_add=True)
