# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-29 10:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0005_person_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='firstName',
        ),
        migrations.RemoveField(
            model_name='person',
            name='lastName',
        ),
        migrations.RemoveField(
            model_name='person',
            name='middleName',
        ),
    ]