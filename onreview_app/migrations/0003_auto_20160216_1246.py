# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 09:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onreview_app', '0002_auto_20160216_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
