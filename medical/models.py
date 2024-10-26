from datetime import timedelta
from django.db import models
import uuid

TREATMENT_TYPE_CHOICES = (
    ('initial_assessment', 'Initial Assessment'),
    ('follow_up', 'Follow-Up'),
    ('therapy', 'Therapy'),
    ('surgery', 'Surgery'),
    ('medication', 'Medication'),
    ('rehabilitation', 'Rehabilitation'),
    ('diagnostic', 'Diagnostic'),
    ('preventive', 'Preventive'),
    ('consultation', 'Consultation'),
)


STATUS_CHOICES = ( 
    ('Pending', 'Pending'),
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)

TEST_TYPE_CHOICES = (
    ('blood_test', 'Blood Test'),
    ('urinalysis', 'Urinalysis'),
    ('imaging', 'Imaging'),
    ('biopsy', 'Biopsy'),
    ('genetic_test', 'Genetic Test'),
    ('culture', 'Culture'),
    ('function_test', 'Function Test'),  # e.g., pulmonary function test
    ('electrocardiogram', 'Electrocardiogram (ECG)'),
    ('x_ray', 'X-Ray'),
    ('ct_scan', 'CT Scan'),
    ('mri', 'MRI'),
    ('ultrasound', 'Ultrasound'),
    ('other', 'Other'),  # For any tests that don't fit the above categories
)

ROUTE_OF_ADMINISTRATION_CHOICES = (
    ('oral', 'Oral'),
    ('intravenous', 'Intravenous'),
    ('intramuscular', 'Intramuscular'),
    ('subcutaneous', 'Subcutaneous'),
    ('topical', 'Topical'),
    ('inhalation', 'Inhalation'),
    ('sublingual', 'Sublingual'),
    ('transdermal', 'Transdermal'),
    ('nasal', 'Nasal'),
    ('ophthalmic', 'Ophthalmic'),
    ('otic', 'Otic'),  # Ear drops
)


class Treatment(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='treatments', limit_choices_to={'role':'Patient'})
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='assessments', limit_choices_to={'role':'Doctor'})
    title = models.CharField(max_length=255)
    treatment_type = models.CharField(max_length=50, choices=TREATMENT_TYPE_CHOICES, default='Oral')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    description = models.TextField()
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    treatment_duration = models.DurationField(blank=True, null=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    medications = models.ManyToManyField('Medication', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
    
    def get_duration(self):
        if self.follow_up_date:
            duration = self.follow_up_date - self.created
            return duration.days  # Returns the duration in days
        return None  # No follow-up date set

    # Optional: To format as a string when follow-up date is missing
    def get_duration_display(self):
        duration = self.get_duration()
        return f"{duration} days" if duration is not None else "Follow-up date not set"



class Tests(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tests', limit_choices_to={'role':'Patient'})  
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='medical_tests', limit_choices_to={'role':'Doctor'})
    title = models.CharField(max_length=255)
    test_type = models.TextField(max_length=255, choices=TEST_TYPE_CHOICES)
    description = models.TextField()
    result = models.CharField(max_length=255, null=True, blank=True)
    result_description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"



class Medication(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    route_of_administration = models.CharField(
        max_length=50,
        choices=ROUTE_OF_ADMINISTRATION_CHOICES
    )
    side_effects = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.dosage})"
