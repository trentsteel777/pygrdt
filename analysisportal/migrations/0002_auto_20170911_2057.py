# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-11 19:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analysisportal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionchain',
            name='stock',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='analysisportal.Stock'),
        ),
    ]
