# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-29 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0003_auto_20171223_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positionsatwork',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]