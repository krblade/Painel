# Generated by Django 3.2.1 on 2021-05-26 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0002_lote_lote_ano'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lote',
            name='lote_dataEnvioLotesLeilao',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='lote',
            name='lote_dataResultadoLeilao',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='lote',
            name='lote_dataSipa',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='lote',
            name='lote_dataSolicitacaoLeilao',
            field=models.CharField(max_length=50),
        ),
    ]