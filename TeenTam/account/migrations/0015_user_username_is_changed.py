# Generated by Django 4.1.1 on 2022-11-10 01:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_remove_user_username_is_changed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username_is_changed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]