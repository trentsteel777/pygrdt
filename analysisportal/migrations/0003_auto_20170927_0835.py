# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-27 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysisportal', '0002_auto_20170911_2057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='option',
            name='nasdaqName',
        ),
        migrations.AddField(
            model_name='option',
            name='expiry',
            field=models.DateField(null=True),
        ),
    ]