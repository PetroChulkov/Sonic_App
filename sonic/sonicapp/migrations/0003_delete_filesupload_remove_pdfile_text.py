# Generated by Django 4.2.5 on 2023-09-21 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sonicapp', '0002_filesupload'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FilesUpload',
        ),
        migrations.RemoveField(
            model_name='pdfile',
            name='text',
        ),
    ]
