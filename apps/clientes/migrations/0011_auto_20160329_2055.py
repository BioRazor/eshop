# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-30 01:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0010_auto_20160126_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compra_envio',
            name='direccion',
            field=models.TextField(blank=True),
        ),
    ]
