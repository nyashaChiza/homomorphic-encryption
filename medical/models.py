from django.db import models
import uuid

ASSESSMENT_CHOICES = (
    ('option 1', 'option 1'),
    ('option 2', 'option 2'),
)

class Treatment(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='treatments', limit_choices_to={'role':'Patient'} )  
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='assessments', limit_choices_to={'role':'Doctor'})
    title = models.CharField(max_length=255)
    assessment_type = models.TextField(max_length=255, choices=ASSESSMENT_CHOICES)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"


class Tests(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tests', limit_choices_to={'role':'Patient'})  
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='medical_tests', limit_choices_to={'role':'Doctor'})
    title = models.CharField(max_length=255)
    test_type = models.TextField(max_length=255, choices=ASSESSMENT_CHOICES)
    description = models.TextField()
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"
