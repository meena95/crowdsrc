# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-11-11 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crowdsrc', '0005_subtask_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtask',
            name='is_right',
            field=models.BooleanField(default=False),
        ),
    ]
