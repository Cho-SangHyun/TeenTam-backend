from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    # django 기본 User Field
    # username, is_staff, is_active, is_superuser, first_name, last_name, last_login, password
    # 필수 기입 필드
    email = models.EmailField(max_length=254, unique=True)
    birth = models.DateField(default=timezone.now)
    # 추가 기입 가능 필드
    profile_image = models.ImageField(
        upload_to="profile_images", default="profile_images/no_profile_image.png")
    postcode = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    detail_address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=15, null=True, unique=True)
    boards_written = models.IntegerField(default=0)
    comments_written = models.IntegerField(default=0)
    username_is_changed = models.DateTimeField(default=timezone.now)
    school = models.CharField(max_length=50, null=True)
    grade = models.CharField(max_length=10, null=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
