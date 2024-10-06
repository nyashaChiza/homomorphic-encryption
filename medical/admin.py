from django.contrib import admin
from .models import Tests, Treatment

class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'assessment_type','title', 'created', 'updated')
    search_fields = ('user', 'patient')
    list_filter = ('doctor','patient','created', 'updated')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

class TestsAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'test_type','title', 'created', 'updated')
    search_fields = ('user', 'patient')
    list_filter = ('doctor','patient', 'created', 'updated')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

# Register models with their respective admin classes
admin.site.register(Tests, TestsAdmin)
admin.site.register(Treatment, TreatmentAdmin)
