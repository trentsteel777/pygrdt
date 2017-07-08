# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optionType', models.CharField(max_length=4)),
                ('nasdaqName', models.CharField(max_length=30)),
                ('contractName', models.CharField(max_length=30)),
                ('last', models.DecimalField(decimal_places=2, max_digits=8)),
                ('change', models.DecimalField(decimal_places=2, max_digits=4)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=8)),
                ('ask', models.DecimalField(decimal_places=2, max_digits=8)),
                ('volume', models.IntegerField()),
                ('openInterest', models.IntegerField()),
                ('strike', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='OptionChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expirationType', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=5)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('nextEarningsDate', models.DateField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='stock',
            name='watchlist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysisportal.Watchlist'),
        ),
        migrations.AddField(
            model_name='optionchain',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysisportal.Stock'),
        ),
        migrations.AddField(
            model_name='option',
            name='optionChain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysisportal.OptionChain'),
        ),
    ]