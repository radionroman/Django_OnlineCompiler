# Generated by Django 4.2 on 2023-04-28 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0004_remove_catalog_availability_changed_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalog',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='file',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
