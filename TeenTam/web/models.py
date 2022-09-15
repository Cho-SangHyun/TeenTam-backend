from django.db import models


class TEST_MODEL(models.Model):
    context = models.CharField(max_length=100, null=True)


class TITLE_MODEL(models.Model):
    title = models.CharField(max_length=100, null=True)
