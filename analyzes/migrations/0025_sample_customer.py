# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-01 03:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0014_auto_20180301_0934'),
        ('analyzes', '0024_auto_20180301_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='customer',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='persons.Customer', verbose_name='Заказчик'),
        ),
    ]
