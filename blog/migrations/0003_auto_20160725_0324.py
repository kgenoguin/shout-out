# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-25 03:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, upload_to=b'pictures'),
        ),
    ]