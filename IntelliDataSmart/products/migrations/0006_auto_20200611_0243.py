# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-11 02:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200610_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productid',
            field=models.PositiveIntegerField(),
        ),
    ]
