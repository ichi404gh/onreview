# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-16 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onreview_app', '0005_auto_20160216_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='code',
            field=models.TextField(default=None, null=True, verbose_name='код'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='description',
            field=models.TextField(default=None, null=True, verbose_name='описание'),
        ),
    ]
