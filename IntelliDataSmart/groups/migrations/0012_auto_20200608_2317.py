# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-08 23:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0011_remove_group_groupid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['pk']},
        ),
    ]