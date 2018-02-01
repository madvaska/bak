# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-01 15:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0007_auto_20180129_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='administrator',
            options={'verbose_name': 'Администратор', 'verbose_name_plural': 'Администраторы'},
        ),
        migrations.AlterModelOptions(
            name='analyst',
            options={'verbose_name': 'Измеритель', 'verbose_name_plural': 'Измерители'},
        ),
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': 'Заказчик', 'verbose_name_plural': 'Заказчики'},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Подразделение', 'verbose_name_plural': 'Подразделения'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Сотрудник', 'verbose_name_plural': 'Сотрудники'},
        ),
        migrations.AlterModelOptions(
            name='positionsatwork',
            options={'verbose_name': 'Занимаемая должность', 'verbose_name_plural': 'Занимаемые должности'},
        ),
        migrations.AlterField(
            model_name='administrator',
            name='addBy',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='administrator_addby', to='persons.Person', verbose_name='Добавлен пользователем '),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.Person', verbose_name='Администратор'),
        ),
        migrations.AlterField(
            model_name='analyst',
            name='addBy',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='analyst_addby', to='persons.Person', verbose_name='Добавлен пользователем'),
        ),
        migrations.AlterField(
            model_name='analyst',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.Person', verbose_name='Измеритель'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='addBy',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='customer_addby', to='persons.Person', verbose_name='Добавлен пользователем'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.Person', verbose_name='Заказчик'),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(blank=True, max_length=100, verbose_name='Название подразделения'),
        ),
        migrations.AlterField(
            model_name='department',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.Department', verbose_name='Родитель'),
        ),
        migrations.AlterField(
            model_name='person',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.Department', verbose_name='Подразделения'),
        ),
        migrations.AlterField(
            model_name='person',
            name='dismissed',
            field=models.DateField(blank=True, null=True, verbose_name='Уволен с '),
        ),
        migrations.AlterField(
            model_name='person',
            name='positionAtWork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.PositionsAtWork', verbose_name='Должность'),
        ),
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='person',
            name='workSince',
            field=models.DateField(verbose_name='Работает с '),
        ),
        migrations.AlterField(
            model_name='positionsatwork',
            name='atDepartment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.Department', verbose_name='Подразделение'),
        ),
        migrations.AlterField(
            model_name='positionsatwork',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='persons.PositionsAtWork', verbose_name='Руководитель'),
        ),
        migrations.AlterField(
            model_name='positionsatwork',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Должность'),
        ),
    ]