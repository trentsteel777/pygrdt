# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysisportal', '0004_auto_20170708_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='nextEarningsDate',
            field=models.CharField(max_length=45, null=True),
        ),
    ]
