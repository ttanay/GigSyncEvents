# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fbprofile',
            name='uri',
            field=models.TextField(null=True),
        ),
    ]
