# Generated by Django 4.2.5 on 2024-02-19 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_jobsubmission_worker_salarypayment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salarypayment',
            name='worker_account',
        ),
    ]
