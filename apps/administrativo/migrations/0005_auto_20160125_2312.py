# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-26 03:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0004_notificacion_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoRecibo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(max_length=50)),
                ('cuenta', models.PositiveSmallIntegerField()),
                ('nro_referencia', models.PositiveSmallIntegerField()),
                ('tipo_pago', models.CharField(choices=[('deposito', 'Deposito'), ('transferencia', 'Transferencia')], default='transferencia', max_length=50)),
                ('fecha_pago', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Factura',
                'verbose_name_plural': 'Facturas',
            },
        ),
        migrations.RenameModel(
            old_name='Factura',
            new_name='Recibo',
        ),
        migrations.RemoveField(
            model_name='pagofactura',
            name='factura',
        ),
        migrations.DeleteModel(
            name='PagoFactura',
        ),
        migrations.AddField(
            model_name='pagorecibo',
            name='recibo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativo.Recibo'),
        ),
    ]
