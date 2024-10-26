# Generated by Django 5.1.1 on 2024-10-26 23:14

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0007_tests_result_tests_result_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('dosage', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=50)),
                ('route_of_administration', models.CharField(choices=[('oral', 'Oral'), ('intravenous', 'Intravenous'), ('intramuscular', 'Intramuscular'), ('subcutaneous', 'Subcutaneous'), ('topical', 'Topical'), ('inhalation', 'Inhalation'), ('sublingual', 'Sublingual'), ('transdermal', 'Transdermal'), ('nasal', 'Nasal'), ('ophthalmic', 'Ophthalmic'), ('otic', 'Otic')], max_length=50)),
                ('side_effects', models.TextField(blank=True, null=True)),
                ('instructions', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='treatment',
            name='diagnosis',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatment',
            name='follow_up_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatment',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50),
        ),
        migrations.AddField(
            model_name='treatment',
            name='symptoms',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='treatment',
            name='treatment_duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='assessment_type',
            field=models.CharField(choices=[('option 1', 'option 1'), ('option 2', 'option 2')], max_length=50),
        ),
        migrations.AddField(
            model_name='treatment',
            name='medications',
            field=models.ManyToManyField(blank=True, to='medical.medication'),
        ),
    ]