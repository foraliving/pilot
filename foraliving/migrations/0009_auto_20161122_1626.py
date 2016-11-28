# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 21:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foraliving', '0008_interview_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='assignment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='foraliving.Assignment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(max_length=128)
        ),
    ]
