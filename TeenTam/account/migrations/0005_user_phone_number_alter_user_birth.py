# Generated by Django 4.1.1 on 2022-09-21 00:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateField(default=datetime.datetime(2022, 9, 21, 0, 51, 8, 663414, tzinfo=datetime.timezone.utc)),
        ),
    ]
