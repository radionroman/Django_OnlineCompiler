# Generated by Django 4.2 on 2023-05-02 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0009_remove_file_catalog_id_file_parent_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.DeleteModel(
            name='Catalog',
        ),
    ]
