# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-19 04:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('persons', '0003_auto_20171223_1330'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analyze',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('comment', models.TextField()),
                ('verifyed', models.BooleanField(default=False)),
                ('analyst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analyst', to='persons.Analyst')),
                ('appointedBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointedBy', to='persons.Analyst')),
            ],
            options={
                'verbose_name': 'Analyze',
                'verbose_name_plural': 'Analyzes',
            },
        ),
        migrations.CreateModel(
            name='AnalyzeDataFormat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('enable', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'AnalyzeDataFormat',
                'verbose_name_plural': 'AnalyzeDataFormats',
            },
        ),
        migrations.CreateModel(
            name='AnalyzeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'OrdesType',
                'verbose_name_plural': 'OrdesTypes',
            },
        ),
        migrations.CreateModel(
            name='DataBinaryValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('value', models.BinaryField()),
                ('analyze', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Analyze')),
            ],
            options={
                'verbose_name': 'dataBinaryValue',
                'verbose_name_plural': 'dataBinaryValues',
            },
        ),
        migrations.CreateModel(
            name='DataFormatField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fieldName', models.CharField(blank=True, max_length=100)),
                ('fieldType', models.CharField(blank=True, choices=[('int', 'int'), ('int', 'int'), ('int', 'int'), ('int', 'int')], default=int, max_length=100)),
                ('serialNumber', models.IntegerField()),
                ('optional', models.BooleanField()),
                ('fieldCaption', models.CharField(blank=True, max_length=100)),
                ('fieldWidth', models.IntegerField()),
                ('fieldWidthInTable', models.IntegerField()),
            ],
            options={
                'verbose_name': 'DataFormatField',
                'verbose_name_plural': 'DataFormatFields',
            },
        ),
        migrations.CreateModel(
            name='DataImageValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('value', models.ImageField(upload_to='')),
                ('analyze', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Analyze')),
                ('dataFormatField', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.DataFormatField')),
            ],
            options={
                'verbose_name': 'dataImageValue',
                'verbose_name_plural': 'dataImageValues',
            },
        ),
        migrations.CreateModel(
            name='dataIntValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('value', models.DecimalField(decimal_places=3, max_digits=10)),
                ('analyze', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Analyze')),
                ('dataFormatField', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.DataFormatField')),
            ],
            options={
                'verbose_name': 'dataIntValue',
                'verbose_name_plural': 'dataIntValues',
            },
        ),
        migrations.CreateModel(
            name='DataTextValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('value', models.TextField()),
                ('analyze', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Analyze')),
                ('dataFormatField', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.DataFormatField')),
            ],
            options={
                'verbose_name': 'dataTextValue',
                'verbose_name_plural': 'dataTextValues',
            },
        ),
        migrations.CreateModel(
            name='DataXLSValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('value', models.FileField(upload_to='')),
                ('analyze', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Analyze')),
                ('dataFormatField', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.DataFormatField')),
            ],
            options={
                'verbose_name': 'dataXLSValue',
                'verbose_name_plural': 'dataXLSValues',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateTime', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('code', models.CharField(blank=True, max_length=100)),
                ('codeOfSample', models.CharField(blank=True, max_length=100)),
                ('comment', models.TextField()),
                ('executed', models.BooleanField(default=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.Customer')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Project'),
        ),
        migrations.AddField(
            model_name='order',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.AnalyzeType'),
        ),
        migrations.AddField(
            model_name='databinaryvalue',
            name='dataFormatField',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.DataFormatField'),
        ),
        migrations.AddField(
            model_name='analyzedataformat',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.AnalyzeType'),
        ),
        migrations.AddField(
            model_name='analyze',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analyzes.Order'),
        ),
    ]
