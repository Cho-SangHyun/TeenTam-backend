# Generated by Django 4.1.1 on 2022-09-28 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_rename_writer_boards_boards_writer_fk_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='content',
            field=models.TextField(blank=True),
        ),
    ]
