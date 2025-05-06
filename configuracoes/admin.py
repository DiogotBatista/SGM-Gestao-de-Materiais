from django.contrib import admin
from .models import Contratante, Contrato, Obra, Empresa_usuario

@admin.register(Contratante)
class ContratanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'ativo', 'data_cadastro', 'get_created_by','data_alteracao', 'get_updated_by')
    search_fields = ('nome', 'cnpj')
    list_filter = ('ativo',)
    ordering = ('nome',)

    def get_created_by(self, obj):
        if obj.created_by:
            # Retorna o nome completo se existir, senão o username
            return obj.created_by.get_full_name() or obj.created_by.username
        return '-'

    get_created_by.short_description = 'Resp. Cadastro'

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return '-'

    get_updated_by.short_description = 'Resp. Atualização'

@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'contratante', 'data_inicio', 'data_fim', 'ativo', 'get_created_by','data_cadastro', 'get_updated_by','data_alteracao')
    search_fields = ('numero', 'contratante__nome')
    list_filter = ('ativo', 'data_inicio', 'data_fim', 'contratante')
    ordering = ('numero',)

    def get_created_by(self, obj):
        if obj.created_by:
            # Retorna o nome completo se existir, senão o username
            return obj.created_by.get_full_name() or obj.created_by.username
        return '-'

    get_created_by.short_description = 'Resp. Cadastro'

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return '-'

    get_updated_by.short_description = 'Resp. Atualização'

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'contrato', 'local', 'data_cadastro','get_created_by', 'data_alteracao', 'get_updated_by','ativo')
    search_fields = ('codigo', 'contrato__numero', 'local')
    list_filter = ('ativo', 'contrato')
    ordering = ('data_cadastro',)

    def get_created_by(self, obj):
        if obj.created_by:
            # Retorna o nome completo se existir, senão o username
            return obj.created_by.get_full_name() or obj.created_by.username
        return '-'

    get_created_by.short_description = 'Resp. Cadastro'

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.get_full_name() or obj.updated_by.username
        return '-'

    get_updated_by.short_description = 'Resp. Atualização'

@admin.register(Empresa_usuario)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('nome', )
