# Generated by Django 3.2.1 on 2021-08-09 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0013_auto_20210717_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprador',
            name='comp_email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='comprador',
            name='comp_cnpj',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]