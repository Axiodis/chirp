# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-21 07:08
from __future__ import unicode_literals

from django.db import migrations, models
import message.models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0004_auto_20170720_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=message.models.get_file_path),
        ),
    ]