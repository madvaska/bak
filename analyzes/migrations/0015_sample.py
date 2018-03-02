# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-08 08:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzes', '0014_deliverysample_setanalyst'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateField(default=datetime.datetime.now, verbose_name='Дата')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Код образца')),
                ('status', models.BooleanField()),
                ('comment', models.TextField()),
            ],
        ),
    ]