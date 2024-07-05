# Generated by Django 5.0.6 on 2024-07-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NyaaaStore', '0005_alter_perfil_city_alter_perfil_direccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='city',
            field=models.CharField(blank=True, choices=[('Santiago', 'Santiago'), ('Valparaíso', 'Valparaíso'), ('Concepción', 'Concepción'), ('Tome', 'Tome'), ('San Pedro', 'San Pedro')], max_length=15),
        ),
        migrations.AlterField(
            model_name='producto',
            name='tp_producto',
            field=models.CharField(choices=[('FIGURA', 'FIGURA'), ('SIN ESPECIFICAR', 'SIN ESPECIFICAR'), ('POLERA', 'POLERA'), ('ACCESORIO', 'ACCESORIO')], default='SIN ESPECIFICAR', max_length=15),
        ),
        migrations.AlterField(
            model_name='venta',
            name='estado',
            field=models.CharField(choices=[('PREPARADO', 'PREPARADO'), ('ENVIADO', 'ENVIADO'), ('EN PREPARACIÓN', 'EN PREPARACIÓN'), ('ENTREGADO', 'ENTREGADO')], default='EN PREPARACIÓN', max_length=30),
        ),
    ]
