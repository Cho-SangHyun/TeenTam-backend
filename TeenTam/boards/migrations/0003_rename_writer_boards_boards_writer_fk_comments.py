# Generated by Django 4.1.1 on 2022-09-28 05:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0002_alter_boardcategories_create_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boards',
            old_name='writer',
            new_name='boards_writer_fk',
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delete_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('like', models.IntegerField(default=0)),
                ('comments_board_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='boards.boards')),
                ('comments_writer_fk', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
