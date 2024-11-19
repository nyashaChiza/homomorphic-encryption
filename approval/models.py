from django.db import models
import uuid

STATUS_CHOICES = (
    ('Granted', 'Granted'),
    ('Denied', 'Denied'),
    ('Pending', 'Pending')
)

class Approval(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='doctors', limit_choices_to={'role': 'Patient'} )  
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='patients')
    comment = models.TextField(blank=True, null=True)
    status = models.TextField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    viewed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['patient', 'doctor'], name='unique_patient_doctor')
        ]

    def __str__(self):
        return f"{self.status}"