# Generated by Django 5.1.1 on 2024-10-06 09:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0004_rename_assessment_treatment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='doctor',
            field=models.ForeignKey(limit_choices_to='role__Doctor', on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='patient',
            field=models.ForeignKey(limit_choices_to='role__Patient', on_delete=django.db.models.deletion.CASCADE, related_name='records', to=settings.AUTH_USER_MODEL),
        ),
    ]
