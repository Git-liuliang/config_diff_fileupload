# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-29 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('nid', models.AutoField(primary_key=True, serialize=False)),
                ('ip_addr', models.CharField(max_length=64, unique=True)),
                ('ssh_port', models.IntegerField()),
                ('app', models.CharField(max_length=64)),
                ('country', models.CharField(max_length=64)),
                ('is_config', models.BooleanField(default=False)),
            ],
        ),
    ]