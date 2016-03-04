# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-14 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comercios', '0005_comercio_agencias'),
        ('clientes', '0002_auto_20160114_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='compra',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='comercios.Producto'),
            preserve_default=False,
        ),
    ]
