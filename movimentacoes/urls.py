from django.urls import path
from .views import (MovimentoListView, MovimentoDetailView, MovimentacaoEntradaCreateView, MovimentacaoSaidaCreateView,
                    MovimentacoesDashboardView, api_materials, MovimentacaoPrintView, GuiaMovimentacaoBrancoView, view_com_erro)
urlpatterns = [
    path('', MovimentacoesDashboardView.as_view(), name='dashboard_movimentacoes'),
    path('lista/', MovimentoListView.as_view(), name='lista_movimentacoes'),
    path('detalhe/<int:pk>/', MovimentoDetailView.as_view(), name='detalhe_movimentacoes'),
    path('cadastrar/entrada/', MovimentacaoEntradaCreateView.as_view(), name='cadastrar_movimentacao_entrada'),
    path('cadastrar/saida/', MovimentacaoSaidaCreateView.as_view(), name='cadastrar_movimentacao_saida'),
    #API materiais
    path('api/materials/', api_materials, name='api_materials'),
    # Impressões
    path('imprimir/<int:pk>/', MovimentacaoPrintView.as_view(), name='movimentacao_print'),
    path('movimentacoes/guia-em-branco/', GuiaMovimentacaoBrancoView.as_view(), name='guia_movimentacao_branco'),

    path('forcar-erro/', view_com_erro, name='forcar_erro'),

]