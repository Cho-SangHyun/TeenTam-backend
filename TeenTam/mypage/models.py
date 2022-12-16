from django.db import models
from account import models as account_models
from boards import models as boards_models
from django.utils import timezone


class Bookmark(models.Model):
    
    bookmark_user_id = models.ForeignKey(account_models.User, on_delete=models.DO_NOTHING, null=False)
    bookmark_boards_id = models.ForeignKey(boards_models.Boards, on_delete=models.CASCADE, null=False)
    bookmark_date = models.DateTimeField(default=timezone.now)