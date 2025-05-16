from django.contrib import admin
from .models import Cargo, Empresa_usuario, UserProfile, ViewDisponivel, PermissaoDeAcessoPorCargo
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.timezone import localtime


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Empresa_usuario)
class EmpresaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'cargo', 'empresa')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('cargo', 'empresa')

@admin.register(ViewDisponivel)
class ViewDisponivelAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(PermissaoDeAcessoPorCargo)
class PermissaoDeAcessoPorCargoAdmin(admin.ModelAdmin):
    list_display = ('cargo',)
    filter_horizontal = ('views',)
    search_fields = ('cargo__nome',)

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'formatted_last_login')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def formatted_last_login(self, obj):
        if obj.last_login:
            return localtime(obj.last_login).strftime('%d/%m/%Y %H:%M')
        return "-"
    formatted_last_login.short_description = 'Último login'

# Substituir o admin padrão do User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customização dos títulos do Admin
admin.site.site_header = "SGM - Sistema de Gestão de Material - Banco de Dados"
admin.site.site_title = "SGM Admin"
admin.site.index_title = "Bem-vindo à gestão do DB do SGM"
