# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_auto_20170501_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dayevent',
            name='hour',
            field=models.DateTimeField(),
        ),
    ]
