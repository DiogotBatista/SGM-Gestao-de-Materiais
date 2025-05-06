from django.urls import path
from .views import MaterialListView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView

urlpatterns = [
    path('', MaterialListView.as_view(), name='lista_materiais'),
    path('cadastrar/', MaterialCreateView.as_view(), name='cadastrar_material'),
    path('editar/<int:pk>/', MaterialUpdateView.as_view(), name='editar_material'),
    path('excluir/<int:pk>/', MaterialDeleteView.as_view(), name='excluir_material'),
]
