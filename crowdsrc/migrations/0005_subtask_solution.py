# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-10 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdsrc', '0004_auto_20161109_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='solution',
            field=models.TextField(default='NULL'),
        ),
    ]
