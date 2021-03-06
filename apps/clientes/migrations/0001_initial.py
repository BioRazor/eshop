# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-14 04:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('ci', models.CharField(blank=True, max_length=50)),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], default='F', max_length=1)),
                ('activo', models.BooleanField(default=True)),
                ('direccion', models.TextField()),
                ('foto_perfil', models.ImageField(upload_to='clientes')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Cliente_Seguir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Cliente')),
            ],
            options={
                'verbose_name': 'Seguido por Cliente',
                'verbose_name_plural': 'Seguidos por Clientes',
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('en_proceso', 'En Proceso'), ('pagado', 'Pagado'), ('enviado', 'Enviado'), ('recibido', 'Recibido')], default='en_proceso', max_length=50)),
                ('fecha_compra', models.DateTimeField(auto_now_add=True)),
                ('tipo_entrega', models.CharField(choices=[('personal', 'Entrega Personal'), ('envio', 'Envio a Direccion')], default='envio', max_length=50)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='Compra_Envio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.TextField()),
                ('detalles', models.TextField(default='Ninguno')),
                ('fecha_recepcion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Compra_Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('deposito', 'Deposito'), ('trans', 'Transferencia')], default='trans', max_length=50)),
                ('fecha_pago', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='compra',
            name='envio',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clientes.Compra_Envio'),
        ),
        migrations.AddField(
            model_name='compra',
            name='pago',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='clientes.Compra_Pago'),
        ),
    ]
