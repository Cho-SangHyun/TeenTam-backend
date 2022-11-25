from django.db import models
from django.utils import timezone
from account import models as account_models


class BoardCategories(models.Model):
    
    name = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=512, null=False)
    create_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(null=True)

    #Foreign key
    manager = models.ForeignKey(account_models.User, on_delete=models.SET_NULL, null=True)


class Boards(models.Model):

    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False)
    
    #null = True or default values
    pub_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)
    image_exist = models.SmallIntegerField(default=0)
    like = models.IntegerField(default=0)
    hit = models.IntegerField(default=0)
    comments_num = models.IntegerField(default=0)
    is_main = models.SmallIntegerField(default=0)
    is_anon = models.BooleanField(default=False)

    #Foreign key
    boards_category = models.ForeignKey(BoardCategories, related_name='boards', on_delete=models.SET_NULL, null=True)
    boards_writer = models.ForeignKey(account_models.User, related_name='boards', on_delete=models.SET_NULL, null=True)

class Comments(models.Model):
    
    content = models.TextField(blank=True, null=False)
    pub_date = models.DateTimeField(default=timezone.now)
    delete_date = models.DateTimeField(null=True)
    modify_date = models.DateTimeField(null=True)
    like = models.IntegerField(default=0)
    
    #foriegn key
    comments_board = models.ForeignKey(Boards, related_name='comments', on_delete=models.DO_NOTHING, null=True)
    comments_writer = models.ForeignKey(account_models.User, related_name='comments', on_delete=models.DO_NOTHING, null = True)
    
    def __str__(self):
        return self.delete_date
    
class Likes(models.Model):
    
    likes_board = models.ForeignKey(Boards, related_name='likes', on_delete=models.DO_NOTHING, null=False)
    likes_user = models.ForeignKey(account_models.User, related_name='likes', on_delete=models.DO_NOTHING, null=False)
    