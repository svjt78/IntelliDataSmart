# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-15 03:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0009_remove_agreement_coverage_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='product',
            field=models.ManyToManyField(to='products.Product'),
        ),
    ]
