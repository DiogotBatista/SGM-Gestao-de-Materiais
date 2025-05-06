from django.urls import path
from .views import painel_relatorios, exportar_excel, exportar_pdf

urlpatterns = [
    path('', painel_relatorios, name='painel_relatorios'),
    path('exportar_excel', exportar_excel, name='exportar_excel'),
    path('exportar_pdf', exportar_pdf, name='exportar_pdf'),
]
