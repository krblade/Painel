# Generated by Django 3.2.1 on 2021-08-12 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0016_lote_lote_vmalote'),
    ]

    operations = [
        migrations.AddField(
            model_name='lote_det',
            name='lode_vmaPercentualLote',
            field=models.FloatField(blank=True, null=True),
        ),
    ]