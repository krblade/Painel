# Generated by Django 3.2.7 on 2021-11-22 22:44

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registros', '0021_auto_20211118_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acomp_tarefa',
            name='tarefa_anotacoes',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
