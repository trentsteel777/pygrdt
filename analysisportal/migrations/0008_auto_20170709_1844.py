# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-09 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysisportal', '0007_auto_20170709_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='nextEarningsDate',
            field=models.DateField(null=True),
        ),
    ]