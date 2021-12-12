# Generated by Django 2.1.5 on 2019-02-19 19:01

import apps.upload.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(default='csv-files/100-data.csv', upload_to='csv-files/', validators=[apps.upload.validator.validate_file_extension])),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]