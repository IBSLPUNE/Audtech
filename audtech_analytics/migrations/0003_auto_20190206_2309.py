# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-07 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audtech_analytics', '0002_auto_20190206_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finaltable',
            name='CreditAmount',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='finaltable',
            name='CreditAmountFC',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='finaltable',
            name='DebitAmount',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='finaltable',
            name='DebitAmountFC',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]