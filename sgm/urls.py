from django.contrib import admin
from django.urls import path, include
from .views import index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('gestao_db/', admin.site.urls),
    # app usuários:
    path('usuarios/', include('usuarios.urls')), #Incluis as URLS de autenticação
    # URLs de autenticação:
    path('login/', auth_views.LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name="logout"),
    # URLs para reset de senha:
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # app materiais
    path('materiais/', include('materiais.urls')),
    # app movimentacoes
    path('movimentacoes/', include('movimentacoes.urls')),
    # app configuracoes
    path('config/', include('configuracoes.urls')),
    # app relatorios
    path('relatorios/', include('relatorios.urls')),

]
