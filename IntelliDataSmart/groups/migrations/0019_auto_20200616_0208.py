# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-16 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0018_auto_20200616_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='groupid',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
