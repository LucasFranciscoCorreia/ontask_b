# Generated by Django 2.1.7 on 2019-03-23 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('action', '0055_action_nrows_all_false'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='nrows_all_false',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='Number of rows with all conditions false'),
        ),
    ]
