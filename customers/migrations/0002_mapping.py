# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-08 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('erp', models.CharField(blank=True, max_length=200, null=True)),
                ('transaction_type', models.CharField(blank=True, max_length=200, null=True)),
                ('final_field', models.CharField(blank=True, max_length=200, null=True)),
                ('source_filed', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
