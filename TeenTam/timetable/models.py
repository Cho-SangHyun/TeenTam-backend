from django.db import models
from account.models import User
# Create your models here.


class TimeTable(models.Model):

    period = models.IntegerField(null=True)
    day = models.IntegerField(null=True)
    subject = models.CharField(max_length=10, null=True)
    timetable_user = models.ForeignKey(
        User, related_name="user_id", on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('day', 'period', 'timetable_user')
