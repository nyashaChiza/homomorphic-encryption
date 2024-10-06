from django.contrib import admin
from .models import Approval

class ApprovalAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'status', 'created', 'updated')
    search_fields = ('doctor', 'patient', 'status')
    list_filter = ('doctor','patient','created', 'updated')
    ordering = ('-created',)
    readonly_fields = ('created', 'updated')

admin.site.register(Approval, ApprovalAdmin)
