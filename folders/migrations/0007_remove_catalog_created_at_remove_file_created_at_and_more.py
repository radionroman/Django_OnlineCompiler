# Generated by Django 4.2 on 2023-05-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0006_alter_filesection_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalog',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='file',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='catalog',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='file',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
