# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-04-01 05:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analyzes', '0031_auto_20180401_1226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='executedDateTime2',
            new_name='executedDateTime',
        ),
    ]
