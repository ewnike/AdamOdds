# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Odds', '0006_auto_20170921_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='betslip',
            name='schedule_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='Odds.ScheduleMLB'),
        ),
    ]