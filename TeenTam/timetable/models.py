from django.db import models
from account import models as account_models

# Create your models here.

class TimeTable(models.Model):
    
    timetable = models.TextField(null=True)
    grade = models.IntegerField(null=False) # 학년
    room = models.IntegerField(null=False) # 반