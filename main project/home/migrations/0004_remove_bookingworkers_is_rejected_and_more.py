# Generated by Django 4.2.5 on 2024-04-17 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_jobsubmission_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookingworkers',
            name='is_rejected',
        ),
        migrations.AddField(
            model_name='bookingworkers',
            name='status',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='salarypayment',
            name='card_holder_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='salarypayment',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.migratoryworker'),
        ),
    ]
