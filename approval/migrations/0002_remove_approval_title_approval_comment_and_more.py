# Generated by Django 5.1.1 on 2024-10-06 10:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approval',
            name='title',
        ),
        migrations.AddField(
            model_name='approval',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='approval',
            name='doctor',
            field=models.ForeignKey(limit_choices_to={'role': 'Doctor'}, on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='approval',
            name='patient',
            field=models.ForeignKey(limit_choices_to={'role': 'Patient'}, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
