# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-18 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0029_auto_20180814_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='action_type',
            field=models.CharField(choices=[('personalized_text', 'Personalized text'), ('personalized_json', 'Personalized JSON'), ('survey', 'Survey'), ('todo_list', 'TODO List')], default='personalized_text', max_length=64),
        ),
    ]