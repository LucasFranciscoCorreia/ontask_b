# Generated by Django 2.2.1 on 2019-05-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0001_squashed_0062_auto_20190521_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
