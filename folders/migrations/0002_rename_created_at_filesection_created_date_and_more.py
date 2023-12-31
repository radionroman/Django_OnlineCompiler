# Generated by Django 4.2 on 2023-04-21 11:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('folders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filesection',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RemoveField(
            model_name='filesection',
            name='end_char',
        ),
        migrations.RemoveField(
            model_name='filesection',
            name='start_char',
        ),
        migrations.AddField(
            model_name='file',
            name='catalog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='folders.catalog'),
        ),
        migrations.AddField(
            model_name='filesection',
            name='file',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='folders.file'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filesection',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='section_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='folders.sectiontype'),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='folders.status'),
        ),
        migrations.AlterField(
            model_name='filesection',
            name='status_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='folders.statusdata'),
        ),
    ]
