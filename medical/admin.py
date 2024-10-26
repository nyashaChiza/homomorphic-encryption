from django.contrib import admin
from .models import Tests, Treatment, Medication


class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage', 'frequency', 'route_of_administration', 'created', 'updated')
    list_filter = ('route_of_administration',)
    search_fields = ('name',)
    ordering = ('name',)
    prepopulated_fields = {'name': ('dosage',)}  # If you want to auto-populate the name


class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'doctor', 'status', 'created', 'updated')
    list_filter = ('status', 'doctor', 'created', 'follow_up_date')
    search_fields = ('title', 'patient__username', 'doctor__username', 'symptoms', 'diagnosis')
    ordering = ('-created',)
    
    # Optional: Customize the form layout
    fieldsets = (
        (None, {
            'fields': ('title', 'patient', 'doctor', 'description', 'symptoms', 'diagnosis')
        }),
        ('Assessment Details', {
            'fields': ('assessment_type', 'status', 'follow_up_date', 'notes')
        }),
        ('Medications', {
            'fields': ('medications',)
        }),
    )
class TestsAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'test_type','title', 'created', 'updated')
    search_fields = ('user', 'patient')
    list_filter = ('doctor','patient', 'created', 'updated')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

# Register models with their respective admin classes
admin.site.register(Tests, TestsAdmin)
admin.site.register(Treatment, TreatmentAdmin)
admin.site.register(Medication, MedicationAdmin)

