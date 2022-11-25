from django.db import models
from account.models import User
# Create your models here.

class Notes(models.Model):
    
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_read = models.DateTimeField(null=True)
    receiver_is_delete = models.DateTimeField(null=True)
    sender_is_delete = models.DateTimeField(null=True)
    delete_date = models.DateTimeField(null=True)