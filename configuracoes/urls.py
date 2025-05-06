from django.urls import path, include
from .views import (MenuView,ContratanteListView, ContratanteCreateView, ContratanteUpdateView, ContratanteDeleteView,
                    ContratosListView, ContratosCreateView, ContratoUpdateView, ContratoDeleteView, ObrasListView,
                    ObrasCreateView, ObrasUpdateView, ObrasDeleteView)


urlpatterns = [
    path('', MenuView.as_view(), name='menu_config'),
    #Contratantes
    path('contratantes/', include([
        path('', ContratanteListView.as_view(), name='lista_contratantes'),
        path('cadastrar/', ContratanteCreateView.as_view(), name='cadastrar_contratante'),
        path('editar/<int:pk>/', ContratanteUpdateView.as_view(), name='editar_contratante'),
        path('excluir/<int:pk>/', ContratanteDeleteView.as_view(), name='excluir_contratante'),
    ])),
    #Contratos
    path('contratos/', include([
        path('', ContratosListView.as_view(), name='lista_contratos'),
        path('cadastrar/', ContratosCreateView.as_view(), name='cadastrar_contratos'),
        path('editar/<int:pk>/', ContratoUpdateView.as_view(), name='editar_contratos'),
        path('excluir/<int:pk>/', ContratoDeleteView.as_view(), name='excluir_contratos'),
    ])),
    #Obras
    path('obras/', include([
        path('', ObrasListView.as_view(), name='lista_obras'),
        path('cadastrar/', ObrasCreateView.as_view(), name='cadastrar_obras'),
        path('editar/<int:pk>/', ObrasUpdateView.as_view(), name='editar_obras'),
        path('excluir/<int:pk>/', ObrasDeleteView.as_view(), name='excluir_obras'),
    ])),
]
