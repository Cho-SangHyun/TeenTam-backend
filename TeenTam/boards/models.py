from django.db import models
from django.utils import timezone
from account import models as account_models


class BoardCategories(models.Model):
    
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=512, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(null=True)

    manager = models.ForeignKey(account_models.User, on_delete=models.SET_NULL, null=True)


class Boards(models.Model):

    pub_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)
    image_exist = models.SmallIntegerField(default=0)
    like = models.IntegerField(default=0)
    hit = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    is_main = models.SmallIntegerField(default=0)

    boarads_category_fk = models.ForeignKey(BoardCategories, on_delete=models.SET_NULL, null=True)
    writer = models.ForeignKey(account_models.User, on_delete=models.SET_NULL, null=True)

