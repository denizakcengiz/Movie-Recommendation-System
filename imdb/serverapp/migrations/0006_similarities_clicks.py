# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 19:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serverapp', '0005_movie_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='similarities',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
    ]
