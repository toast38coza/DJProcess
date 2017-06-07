# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-07 12:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('process_id', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('N', 'New'), ('X', 'Cancelled'), ('C', 'Complete'), ('F', 'Failed'), ('XF', 'Cancelled Failed')], default='N', max_length=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('request_data', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.CharField(max_length=255)),
                ('input_data', models.TextField(default='{}')),
                ('result_data', models.TextField(default='{}')),
                ('status', models.CharField(choices=[('N', 'New'), ('X', 'Cancelled'), ('C', 'Complete'), ('F', 'Failed'), ('XF', 'Cancelled Failed')], default='N', max_length=10)),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.Process')),
            ],
        ),
    ]
