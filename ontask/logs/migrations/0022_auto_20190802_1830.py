# Generated by Django 2.2.3 on 2019-08-02 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0021_auto_20190609_1325'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='log',
            options={'verbose_name': 'log', 'verbose_name_plural': 'logs'},
        ),
        migrations.AlterModelTable(
            name='log',
            table='log',
        ),
    ]