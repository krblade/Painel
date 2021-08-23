# Generated by Django 3.2.1 on 2021-07-17 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0012_auto_20210705_0953'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprador',
            name='comp_celular',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comprador',
            name='comp_cidade',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comprador',
            name='comp_endereco',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comprador',
            name='comp_telefoneComercial',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='comprador',
            name='comp_telefoneResidencial',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='disputa_aberta',
            name='diab_lanceTotal',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='disputa_aberta',
            name='diab_lanceUnitario',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='comprador',
            name='comp_cnpj',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comprador',
            name='comp_codigoSap',
            field=models.BigIntegerField(null=True),
        ),
    ]