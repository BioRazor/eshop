# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-27 02:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comercios', '0009_auto_20160125_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto_fotos',
            name='foto0',
            field=models.ImageField(upload_to='productos', verbose_name='1ra Foto'),
        ),
        migrations.AlterField(
            model_name='producto_fotos',
            name='foto1',
            field=models.ImageField(upload_to='productos', verbose_name='2da Foto'),
        ),
        migrations.AlterField(
            model_name='producto_fotos',
            name='foto2',
            field=models.ImageField(upload_to='productos', verbose_name='3ra Foto'),
        ),
        migrations.AlterField(
            model_name='producto_fotos',
            name='foto3',
            field=models.ImageField(upload_to='productos', verbose_name='4ta Foto'),
        ),
    ]
