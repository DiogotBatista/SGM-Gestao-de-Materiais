from django.contrib import admin
from .models import Unidade, GrupoMaterial, Material

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('unidade', 'descricao', 'ativo')
    search_fields = ('unidade',)
    list_filter = ('ativo',)
    ordering = ('unidade',)

@admin.register(GrupoMaterial)
class GrupoMaterialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo')
    search_fields = ('nome',)
    list_filter = ('ativo',)
    ordering = ('nome',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'saldo_inicial',
        'saldo_atual',
        'unidade',
        'grupo',
        'armazenagem',
        'ativo',
        'get_created_by',
        'data_cadastro',
        'get_updated_by',
        'data_alteracao'

    )
    search_fields = ('nome',)
    list_filter = ('ativo', 'unidade', 'grupo', 'data_cadastro', 'armazenagem')
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

