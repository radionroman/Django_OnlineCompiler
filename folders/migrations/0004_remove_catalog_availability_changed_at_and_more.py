# Generated by Django 4.2 on 2023-04-28 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0003_rename_catalog_file_catalog_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='availability_changed_at',
        ),
        migrations.RemoveField(
            model_name='catalog',
            name='last_content_changed_at',
        ),
        migrations.RemoveField(
            model_name='file',
            name='availability_changed_at',
        ),
        migrations.RemoveField(
            model_name='file',
            name='last_content_changed_at',
        ),
        migrations.RemoveField(
            model_name='filesection',
            name='created_date',
        ),
    ]
