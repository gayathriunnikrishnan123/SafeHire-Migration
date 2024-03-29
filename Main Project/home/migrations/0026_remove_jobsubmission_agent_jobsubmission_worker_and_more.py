# Generated by Django 4.2.5 on 2024-02-14 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_alter_jobsubmission_agent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobsubmission',
            name='agent',
        ),
        migrations.AddField(
            model_name='jobsubmission',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.migratoryworker'),
        ),
        migrations.AlterField(
            model_name='jobsubmission',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
