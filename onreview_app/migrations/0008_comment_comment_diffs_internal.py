# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 12:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onreview_app', '0007_auto_20160217_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment_diffs_internal',
            field=models.TextField(blank=True, default=''),
        ),
    ]
