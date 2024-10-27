from django.contrib import admin
from .models import Approval

class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'status', 'viewed','created', 'updated')
    search_fields = ('doctor', 'patient', 'status', 'viewed')
    list_filter = ('doctor','patient','created', 'updated', 'viewed')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

admin.site.register(Approval, ApprovalAdmin)
