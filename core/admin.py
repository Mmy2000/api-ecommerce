from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth import get_user_model
# from django.utils.translation import ugettext_lazy as _  # Commented out since it's not being used in your example

# Unregister the default User model from the auth app
admin.site.unregister(get_user_model())

class CustomUserAdmin(DefaultUserAdmin):
    """Define admin model for custom User model with no username field."""
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('id','email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register your custom User model with the custom UserAdmin
admin.site.register(get_user_model(), CustomUserAdmin)
