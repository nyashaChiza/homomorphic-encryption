from datetime import timedelta
from django.db import models
import uuid

TREATMENT_TYPE_CHOICES = (
    ('Initial Assessment', 'Initial Assessment'),
    ('Follow Up', 'Follow Up'),
    ('Therapy', 'Therapy'),
    ('Surgery', 'Surgery'),
    ('Medication', 'Medication'),
    ('Rehabilitation', 'Rehabilitation'),
    ('Diagnostic', 'Diagnostic'),
    ('Preventive', 'Preventive'),
    ('Consultation', 'Consultation'),
)

STATUS_CHOICES = ( 
    ('Pending', 'Pending'),
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)

TEST_TYPE_CHOICES = (
    ('Blood Test', 'Blood Test'),
    ('Urinalysis', 'Urinalysis'),
    ('Imaging', 'Imaging'),
    ('Biopsy', 'Biopsy'),
    ('Genetic Test', 'Genetic Test'),
    ('Culture', 'Culture'),
    ('Function Test', 'Function Test'),  # e.g., pulmonary function test
    ('Electrocardiogram', 'Electrocardiogram (ECG)'),
    ('X-Ray', 'X-Ray'),
    ('CT-Scan', 'CT-Scan'),
    ('MRI', 'MRI'),
    ('Ultrasound', 'Ultrasound'),
    ('Other', 'Other'),  # For any tests that don't fit the above categories
)

ROUTE_OF_ADMINISTRATION_CHOICES = (
    ('Oral', 'Oral'),
    ('Intravenous', 'Intravenous'),
    ('Intramuscular', 'Intramuscular'),
    ('Subcutaneous', 'Subcutaneous'),
    ('Topical', 'Topical'),
    ('Inhalation', 'Inhalation'),
    ('Sublingual', 'Sublingual'),
    ('Transdermal', 'Transdermal'),
    ('Nasal', 'Nasal'),
    ('Ophthalmic', 'Ophthalmic'),
    ('Otic', 'Otic'),  # Ear drops
)

FREQUENCY_CHOICES = (
    ('Once', 'Once'),
    ('Twice', 'Twice'),
    ('Thrice', 'Thrice'),
)


class Treatment(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='treatments', limit_choices_to={'role':'Patient'})
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='assessments')
    title = models.CharField(max_length=255)
    treatment_type = models.CharField(max_length=50, choices=TREATMENT_TYPE_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    description = models.TextField()
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    medications = models.ManyToManyField('Medication', blank=True, related_name='medicine')
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
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='medical_tests')
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
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES)
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


class TreatmentMedication(models.Model):
    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE,
        related_name='treatment_medications'
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name='treatment_medications'
    )
    method_of_administration = models.CharField(max_length=255)
    quantity = models.IntegerField()
    frequency = models.CharField(max_length=50)

    class Meta:
        unique_together = ('treatment', 'medication')  # Prevent duplicate entries

    def __str__(self):
        return f"{self.medication.name} for {self.treatment.title}"