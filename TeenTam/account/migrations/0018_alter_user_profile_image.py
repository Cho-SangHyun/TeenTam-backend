# Generated by Django 4.1.1 on 2022-12-06 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_user_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='profile_images/no_profile_image.png', upload_to='profile_images/%Y/%m/%d'),
        ),
    ]