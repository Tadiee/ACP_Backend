# Generated by Django 4.2 on 2025-06-24 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_files', '0004_alter_system_files_created_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_files',
            name='file_type',
            field=models.CharField(default='pdf', max_length=100),
        ),
    ]
