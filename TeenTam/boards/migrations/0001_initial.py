# Generated by Django 4.1.1 on 2022-09-29 03:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=512)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delete_date', models.DateTimeField(null=True)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Boards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delete_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('image_exist', models.SmallIntegerField(default=0)),
                ('like', models.IntegerField(default=0)),
                ('hit', models.IntegerField(default=0)),
                ('comments_num', models.IntegerField(default=0)),
                ('is_main', models.SmallIntegerField(default=0)),
                ('boards_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boards', to='boards.boardcategories')),
                ('boards_writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='boards', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('delete_date', models.DateTimeField(null=True)),
                ('modify_date', models.DateTimeField(null=True)),
                ('like', models.IntegerField(default=0)),
                ('comments_board', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='comments', to='boards.boards')),
                ('comments_writer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]