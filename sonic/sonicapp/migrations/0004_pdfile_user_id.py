# Generated by Django 4.2.5 on 2023-09-22 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sonicapp', '0003_delete_filesupload_remove_pdfile_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdfile',
            name='user_id',
            field=models.ForeignKey(default=150, on_delete=django.db.models.deletion.CASCADE, related_name='pdfile', to=settings.AUTH_USER_MODEL),
        ),
    ]
