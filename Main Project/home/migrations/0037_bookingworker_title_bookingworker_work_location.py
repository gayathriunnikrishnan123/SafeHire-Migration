# Generated by Django 4.2.5 on 2024-02-20 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0036_salarypayment_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingworker',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bookingworker',
            name='work_location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
