# Generated by Django 5.1.1 on 2024-10-26 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0008_medication_treatment_diagnosis_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatment',
            name='assessment_type',
        ),
        migrations.AddField(
            model_name='treatment',
            name='treatment_type',
            field=models.CharField(choices=[('initial_assessment', 'Initial Assessment'), ('follow_up', 'Follow-Up'), ('therapy', 'Therapy'), ('surgery', 'Surgery'), ('medication', 'Medication'), ('rehabilitation', 'Rehabilitation'), ('diagnostic', 'Diagnostic'), ('preventive', 'Preventive'), ('consultation', 'Consultation')], default='Oral', max_length=50),
        ),
        migrations.AlterField(
            model_name='tests',
            name='test_type',
            field=models.TextField(choices=[('blood_test', 'Blood Test'), ('urinalysis', 'Urinalysis'), ('imaging', 'Imaging'), ('biopsy', 'Biopsy'), ('genetic_test', 'Genetic Test'), ('culture', 'Culture'), ('function_test', 'Function Test'), ('electrocardiogram', 'Electrocardiogram (ECG)'), ('x_ray', 'X-Ray'), ('ct_scan', 'CT Scan'), ('mri', 'MRI'), ('ultrasound', 'Ultrasound'), ('other', 'Other')], max_length=255),
        ),
    ]
