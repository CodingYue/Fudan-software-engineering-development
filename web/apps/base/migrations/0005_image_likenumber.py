# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-16 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20161213_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='likenumber',
            field=models.IntegerField(default=0),
        ),
    ]
