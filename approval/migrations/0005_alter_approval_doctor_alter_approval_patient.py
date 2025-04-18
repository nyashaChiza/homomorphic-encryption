# Generated by Django 5.1.1 on 2024-11-15 07:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval', '0004_approval_viewed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='approval',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to=settings.AUTH_USER_MODEL),
        ),
    ]
