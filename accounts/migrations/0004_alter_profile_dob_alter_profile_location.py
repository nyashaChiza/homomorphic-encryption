# Generated by Django 5.1.1 on 2025-01-26 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_location_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(choices=[('Harare West', 'Harare West'), ('Harare East', 'Harare East'), ('Harare North', 'Harare North'), ('Harare South', 'Harare South'), ('Other', 'Other')], max_length=40),
        ),
    ]
