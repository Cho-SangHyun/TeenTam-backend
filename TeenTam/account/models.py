from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
# Create your models here.


class User(AbstractUser):
    pass


# # Create Token for each user
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)