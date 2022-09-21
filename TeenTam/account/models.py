from datetime import date
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    # 필수 기입 필드
    email = models.EmailField(max_length=254, unique=True)
    birth = models.DateField(default=timezone.now())
    # 추가 기입 가능 필드
    profile_image = models.ImageField(upload_to="profile_images", default = "profile_images/no_profile_image.png")
    postcode = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    detail_address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


# # Create Token for each user
# for user in User.objects.all():
#     Token.objects.get_or_create(user=user)