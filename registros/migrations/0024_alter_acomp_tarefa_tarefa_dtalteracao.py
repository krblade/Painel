# Generated by Django 3.2.7 on 2021-11-24 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0023_auto_20211123_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acomp_tarefa',
            name='tarefa_dtalteracao',
            field=models.DateTimeField(default='2021-11-02 22:45:24', editable=False),
            preserve_default=False,
        ),
    ]
