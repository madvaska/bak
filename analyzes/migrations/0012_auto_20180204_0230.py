# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-03 19:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('analyzes', '0011_auto_20180204_0229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataformatfield',
            name='dataFormat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.DataFormat', verbose_name='Формат данных'),
        ),
    ]
