# Generated by Django 2.2.5 on 2019-09-09 01:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ontask', '0019_auto_20190909_0747'),
    ]

    operations = [
        migrations.CreateModel(
            name='RubricCell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=512, verbose_name='level of attainment')),
                ('description_text', models.CharField(blank=True, default='', max_length=2048, verbose_name='description')),
                ('feedback_text', models.CharField(blank=True, default='', max_length=2048, verbose_name='feedback')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rubric_cells', to='ontask.Action')),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rubric_cells', to='ontask.Column')),
            ],
            options={
                'ordering': ['column__position'],
                'unique_together': {('action', 'column', 'category')},
            },
        ),
    ]