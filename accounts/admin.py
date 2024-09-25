from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.contrib.auth.models import User as AuthUser


# Define the UserAdmin to customize user management in the admin panel
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # List the fields that will be displayed in the admin list view
    list_display = ('uuid', 'username', 'first_name', 'last_name', 'email', 'role', 'is_active', 'is_staff', 'created', 'updated')
    
    # Enable searching by relevant fields
    search_fields = ('username', 'first_name', 'last_name', 'email', 'role')
    
    # Filters to quickly narrow down users by role and status
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    
    # Fields to display when viewing or editing a user
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Timestamps', {'fields': ('created', 'updated')}),
    )
    
    # Fields to display when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    # Specify read-only fields
    readonly_fields = ('created', 'updated')
    
    # Default ordering in the admin panel
    ordering = ('-created',)
    
    # Allow the custom form for adding/editing users
    add_form_template = 'admin/auth/user/add_form.html'


# Define the ProfileAdmin to customize profile management in the admin panel
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Fields to display in the list view for profiles
    list_display = ('uuid', 'user', 'gender', 'contact', 'dob', 'emergency_contact', 'created', 'updated')
    
    # Enable searching by user details and profile-specific fields
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'contact', 'gender', 'dob')
    
    # Filters to quickly narrow down profiles by gender or created/updated timestamps
    list_filter = ('gender', 'created', 'updated')
    
    # Fields to display when viewing or editing a profile
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Profile Info', {'fields': ('gender', 'address', 'contact', 'dob', 'emergency_contact')}),
        ('Timestamps', {'fields': ('created', 'updated')}),
    )
    
    # Read-only fields for timestamps
    readonly_fields = ('created', 'updated')
    
    # Default ordering for profiles
    ordering = ('-created',)

    # Enable inline editing of User profile fields from the UserAdmin
    raw_id_fields = ('user',)  # Use raw ID widget to select users in the profile form
