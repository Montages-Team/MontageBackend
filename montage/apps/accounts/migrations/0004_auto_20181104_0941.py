# Generated by Django 2.1.2 on 2018-11-04 00:41

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20181104_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='montageuser',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]