# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-11 03:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0002_auto_20200611_0340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='agreement_date',
        ),
    ]