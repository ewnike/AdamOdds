# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Odds', '0004_auto_20170917_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betslip',
            name='schedule_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='Odds.ScheduleMLB'),
        ),
    ]
