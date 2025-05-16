# sgm/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import Empresa_usuario
from configuracoes.models import Aviso

@login_required
def index(request):
    avisos = Aviso.objects.filter(ativo=True).order_by('-criado_em')
    empresa = None
    if hasattr(request.user, 'userprofile'):
        empresa = request.user.userprofile.empresa
    return render(request, 'index.html', {'avisos': avisos, 'empresa': empresa})

