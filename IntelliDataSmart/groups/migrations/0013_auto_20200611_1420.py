# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2020-06-11 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0012_auto_20200608_2317'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-group_date']},
        ),
        migrations.AddField(
            model_name='group',
            name='group_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.CharField(default='User', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='group',
            unique_together=set([('slug', 'purpose', 'group_date')]),
        ),
    ]
