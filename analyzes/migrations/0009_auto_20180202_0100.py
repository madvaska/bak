# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-01 18:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyzes', '0008_auto_20180202_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=100, unique=True, verbose_name='Код заявки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='codeOfSample',
            field=models.CharField(max_length=100, unique=True, verbose_name='Код образца'),
        ),
        migrations.AlterField(
            model_name='orderscode',
            name='code',
            field=models.CharField(max_length=100, unique=True, verbose_name='Код заявки'),
        ),
        migrations.AlterField(
            model_name='samplescode',
            name='codeOfSample',
            field=models.CharField(max_length=100, unique=True, verbose_name='Код образца'),
        ),
    ]