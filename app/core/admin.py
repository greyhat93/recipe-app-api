"""Django admin customerize."""
from django.contrib import admin # noqa
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as lazy

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields':('email','password')}),
        (
            lazy('Permissions'),
            {
                'fields':(
                        'is_active',
                        'is_staff',
                        'is_superuser'
                )
            }
        ),
        (lazy('Important dates'), {'fields':('last_login',)}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (
        None,{
            'classes':('wide',),
            'fields' :(
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

admin.site.register(User, UserAdmin)
