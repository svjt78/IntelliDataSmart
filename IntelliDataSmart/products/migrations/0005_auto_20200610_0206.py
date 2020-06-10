# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-10 02:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200610_0131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price_per_1000_dollars',
            new_name='price_per_1000_units',
        ),
        migrations.RemoveField(
            model_name='product',
            name='coverage_limit',
        ),
    ]