from django.db import models
from account.models import User
from django.utils import timezone
# Create your models here.


class Notes(models.Model):

    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="receiver")
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sender")
    content = models.TextField(null=True)
    send_date = models.DateTimeField(default=timezone.now)
    is_read = models.DateTimeField(null=True)
    sender_is_delete = models.DateTimeField(null=True)
    receiver_is_delete = models.DateTimeField(null=True)
    delete_date = models.DateTimeField(null=True)
