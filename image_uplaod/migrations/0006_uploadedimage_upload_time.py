# Generated by Django 5.0 on 2023-12-10 20:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_uplaod', '0005_alter_uploadedimage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedimage',
            name='upload_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
