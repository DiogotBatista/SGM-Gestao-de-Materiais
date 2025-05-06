from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class CustomUserAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login', 'display_cargo', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets

    def display_cargo(self, obj):
        return obj.cargo
    display_cargo.short_description = 'Cargo'

admin.site.register(Usuario, CustomUserAdmin)

from django.contrib import admin

admin.site.site_header = "SGM - Sistema de Gestão de Material - Banco de Dados"
admin.site.site_title = "SGM Admin"
admin.site.index_title = "Bem-vindo à gestão do DB do SGM"
