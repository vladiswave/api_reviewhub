from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

from users.models import YamdbUser


class AdminFormPasswordValidation(forms.ModelForm):
    """Форма для изменения и валидации пароля администратором."""

    class Meta:
        model = YamdbUser
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
            return make_password(password)
        return password


@admin.register(YamdbUser)
class UserAdminYamdb(UserAdmin):
    """Админ-зона с новыми полями."""

    form = AdminFormPasswordValidation
    list_display = ('username', 'email', 'first_name', 'last_name', 'role',)
    list_filter = ('role', )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('username', 'email', 'bio', 'role')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
