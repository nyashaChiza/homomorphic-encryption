# Generated by Django 5.1.1 on 2024-11-25 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, choices=[('Harare West', 'Harare West'), ('Harare East', 'Harare East'), ('Harare North', 'Harare North'), ('Harare South', 'Harare South'), ('Other', 'Other')], max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Clerk', 'Clerk'), ('Admin', 'Admin'), ('Researcher', 'Researcher')], max_length=20),
        ),
    ]
