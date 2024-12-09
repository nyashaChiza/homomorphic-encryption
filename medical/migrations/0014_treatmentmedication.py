# Generated by Django 5.1.1 on 2024-12-09 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0013_alter_treatment_medications'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentMedication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method_of_administration', models.CharField(max_length=255)),
                ('quantity', models.IntegerField()),
                ('frequency', models.CharField(max_length=50)),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment_medications', to='medical.medication')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatment_medications', to='medical.treatment')),
            ],
            options={
                'unique_together': {('treatment', 'medication')},
            },
        ),
    ]