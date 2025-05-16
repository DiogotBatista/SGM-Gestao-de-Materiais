from django.urls import path
from .views import UsuarioListView, UsuarioCreateView, UsuarioUpdateView, UsuarioDeleteView, CustomPasswordResetConfirmView

urlpatterns = [
    path('', UsuarioListView.as_view(), name='lista_usuarios'),
    path('cadastrar/', UsuarioCreateView.as_view(), name='cadastrar_usuario'),
    path('editar/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),
    path('excluir/<int:pk>/', UsuarioDeleteView.as_view(), name='excluir_usuario'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
]
