# sgm/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from configuracoes.models import Empresa_usuario

@login_required
def index(request):
    # Considerando que exista somente um registro, usamos first()
    empresa = Empresa_usuario.objects.first()
    return render(request, 'index.html', {'empresa': empresa})
