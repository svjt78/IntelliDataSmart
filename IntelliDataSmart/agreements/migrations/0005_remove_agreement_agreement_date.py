# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-11 04:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agreements', '0004_agreement_agreement_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='agreement_date',
        ),
    ]