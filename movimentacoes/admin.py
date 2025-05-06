from django.contrib import admin
from .models import Movimentacao, MovimentoItem

class MovimentoItemInline(admin.TabularInline):
    model = MovimentoItem
    extra = 1
    fields = ('material', 'tipo', 'quantidade')
    # Se preferir, você pode tornar 'tipo' somente leitura, já que é definido automaticamente
    readonly_fields = ('tipo',)
    can_delete = True

@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'obra', 'documento', 'data_movimentacao', 'realizado_por_full_name', 'tipo')
    list_filter = ('obra', 'data_movimentacao')
    search_fields = ('codigo', 'documento', 'obra__nome')
    ordering = ('-data_movimentacao',)
    inlines = [MovimentoItemInline]

    def realizado_por_full_name(self, obj):
        """
        Retorna o nome completo do usuário que realizou a movimentação.
        Se não houver nome completo, retorna o username.
        """
        if obj.realizado_por:
            full_name = obj.realizado_por.get_full_name()
            return full_name if full_name else obj.realizado_por.username
        return "-"
    realizado_por_full_name.short_description = "Realizado Por"

@admin.register(MovimentoItem)
class MovimentoItemAdmin(admin.ModelAdmin):
    list_display = ('movimentacao_codigo', 'material', 'tipo_display', 'quantidade')
    list_filter = ('tipo', 'material')
    search_fields = ('movimentacao__codigo', 'material__nome')
    ordering = ('material',)

    def movimentacao_codigo(self, obj):
        return obj.movimentacao.codigo
    movimentacao_codigo.short_description = "Movimentação"

    def tipo_display(self, obj):
        return obj.get_tipo_display()
    tipo_display.short_description = "Tipo de Movimentação"
