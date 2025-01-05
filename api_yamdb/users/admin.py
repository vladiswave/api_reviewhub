from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import YamdbUser


@admin.register(YamdbUser)
class UserAdminYamdb(UserAdmin):
    """Админ-зона с новыми полями."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'role',)
    list_editable = ('role', )
    list_filter = ('role', )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'email', 'bio', 'role')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
