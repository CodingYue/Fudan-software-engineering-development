# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-14 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=5000)),
                ('file', models.FileField(upload_to=b'repository/%Y/%m/%d')),
            ],
        ),
    ]
