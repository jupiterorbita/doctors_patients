# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-25 23:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
        ('doctor', '0002_auto_20180524_1458'),
    ]

    operations = [
        migrations.CreateModel(
            name='patients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patient.patients')),
            ],
        ),
    ]
