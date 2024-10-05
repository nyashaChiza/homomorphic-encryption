from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

ROLE_CHOICES = (
    ('Patient', 'Patient'),
    ('Doctor', 'Doctor'),
    ('Clerk', 'Clerk'),
    ('Admin', 'Admin')
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid

ROLE_CHOICES = (
    ('Patient', 'Patient'),
    ('Doctor', 'Doctor'),
    ('Clerk', 'Clerk'),
    ('Admin', 'Admin')
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

class User(AbstractUser):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    role = models.CharField(choices=ROLE_CHOICES, max_length=20)

    # Add related_name to avoid clashes with the auth.User model
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Add a custom related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Add a custom related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_initials(self):
        return f"{self.first_name[0]} {self.last_name[0]}"


class Profile(models.Model):
    uuid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # One-to-One relationship
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)  # Reduced max_length for gender
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)  # Contact field with realistic length
    dob = models.DateField(blank=True, null=True)  # Date of birth
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)  # Emergency contact field
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    
