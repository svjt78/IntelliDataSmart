# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-08 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_auto_20200608_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='groupid',
            field=models.CharField(blank=True, default='[737156]', editable=False, max_length=6),
        ),
    ]