from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import Group

def has_access(user, allowed_roles):
    """
    Retorna True se o usuário for superusuário ou pertencer a pelo menos um dos grupos permitidos.
    Se allowed_roles estiver vazia, serão considerados todos os grupos existentes.
    """
    if user.is_superuser:
        return True
    if not allowed_roles:
        allowed_roles = list(Group.objects.values_list('name', flat=True))
    return user.groups.filter(name__in=allowed_roles).exists()

class AccessRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = []  # Grupos permitidos
    no_permission_redirect_url = 'index'  # URL padrão para redirecionamento

    def test_func(self):
        return has_access(self.request.user, self.allowed_roles)

    def handle_no_permission(self):
        messages.warning(self.request, "Acesso não autorizado.")
        return redirect(self.no_permission_redirect_url)
