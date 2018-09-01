from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts import models


class UserAdmin(BaseUserAdmin):

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Organizations', {'fields': ('organizations', 'default_organization')}),
    )

    ordering = ('email',)
    list_display = ('email', 'full_name', 'is_staff')

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')



admin.site.register(models.User, UserAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
