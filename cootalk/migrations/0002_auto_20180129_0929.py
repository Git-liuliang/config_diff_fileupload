# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-29 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cootalk', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='config_dir',
            field=models.CharField(default='/usr/local/tomcat/', max_length=256),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='ip_addr',
            field=models.CharField(max_length=64),
        ),
    ]