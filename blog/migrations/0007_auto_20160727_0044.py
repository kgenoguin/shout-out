# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-27 00:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20160726_0811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='blog.Post')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
