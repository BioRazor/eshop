# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-26 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0007_auto_20160126_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificacion',
            name='destinatario',
            field=models.CharField(default='nada', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notificacion',
            name='id_destinatario',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
