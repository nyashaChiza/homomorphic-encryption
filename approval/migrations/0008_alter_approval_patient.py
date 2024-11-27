# Generated by Django 5.1.1 on 2024-11-17 13:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0007_merge_20241117_1519'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='patient',
            field=models.ForeignKey(limit_choices_to={'role': 'Patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to=settings.AUTH_USER_MODEL),
        ),
    ]