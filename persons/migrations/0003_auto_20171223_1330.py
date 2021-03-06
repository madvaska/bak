# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-23 13:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0002_auto_20171223_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrator',
            name='addBy',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='administrator_addby', to='persons.Person'),
        ),
        migrations.AddField(
            model_name='analyst',
            name='addBy',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='analyst_addby', to='persons.Person'),
        ),
        migrations.AddField(
            model_name='customer',
            name='addBy',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='customer_addby', to='persons.Person'),
        ),
    ]
