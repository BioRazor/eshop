# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-26 00:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administrativo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PagoFactura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banco', models.CharField(max_length=50)),
                ('cuenta', models.PositiveSmallIntegerField()),
                ('nro_referencia', models.PositiveSmallIntegerField()),
                ('tipo_pago', models.CharField(choices=[('deposito', 'Deposito'), ('transferencia', 'Transferencia')], default='transferencia', max_length=50)),
                ('fecha_pago', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='duracion',
            new_name='fecha_fin',
        ),
        migrations.RenameField(
            model_name='factura',
            old_name='fecha',
            new_name='fecha_inicio',
        ),
        migrations.RemoveField(
            model_name='factura',
            name='administrador',
        ),
        migrations.AddField(
            model_name='factura',
            name='estado',
            field=models.CharField(choices=[('por cancelar', 'En espera de Pago'), ('por verificar pago', 'Es espera de verificación'), ('pagado', 'Pagado'), ('vencido', 'Vencido')], default='por cancelar', max_length=50),
        ),
        migrations.AddField(
            model_name='factura',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='factura',
            name='precio',
            field=models.PositiveSmallIntegerField(default=30000),
        ),
        migrations.AddField(
            model_name='pagofactura',
            name='factura',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrativo.Factura'),
        ),
    ]
