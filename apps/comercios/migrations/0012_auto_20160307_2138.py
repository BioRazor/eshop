# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercios', '0011_auto_20160126_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comercio_telefono',
            name='telefono',
            field=models.PositiveIntegerField(),
        ),
    ]
