from django import template

register = template.Library()

@register.filter
def has_access(patient, doctor):
    return patient.has_access(doctor)
