# Generated by Django 4.1.1 on 2022-12-20 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timetable', '0004_alter_timetable_timetable_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='timetable_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
