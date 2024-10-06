from django.db import models
import uuid

STATUS_CHOICES = (
    ('Granted', 'Granted'),
    ('Denied', 'Denied'),
    ('Pending', 'Pending')
)

class Approval(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    patient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='owner', limit_choices_to={'role':'Patient'} )  
    doctor = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='requester', limit_choices_to={'role':'Doctor'})
    comment = models.TextField(blank=True, null=True)
    status = models.TextField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.status}"