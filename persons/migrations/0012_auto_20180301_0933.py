# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-01 02:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0011_auto_20180202_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='persons.Person', verbose_name='Администратор'),
        ),
    ]
