# Generated by Django 2.2 on 2019-04-30 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0004_auto_20180511_1528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='view',
            options={'ordering': ['name']},
        ),
    ]