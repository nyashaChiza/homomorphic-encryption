# Generated by Django 5.1.1 on 2024-12-09 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0014_treatmentmedication'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatment',
            name='medications',
        ),
    ]
