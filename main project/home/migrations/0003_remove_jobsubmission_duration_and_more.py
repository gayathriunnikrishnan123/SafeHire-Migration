# Generated by Django 4.2.5 on 2024-04-04 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_jobsubmission_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobsubmission',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='jobsubmission',
            name='work_location',
        ),
    ]
