# Generated by Django 3.2.1 on 2021-06-14 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0007_alter_lote_his_lohi_retirada'),
    ]

    operations = [
        migrations.CreateModel(
            name='TESTES',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testeA', models.CharField(max_length=50, null=True)),
                ('testeB', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]