from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Usuario
from .forms import UsuarioCreationForm, UsuarioChangeForm
from django.contrib import messages
from .mixins import AccessRequiredMixin
from django.db.models import Q

class UsuarioListView(AccessRequiredMixin, ListView):
    allowed_roles = ['Gestor']
    model = Usuario
    template_name = 'usuarios/lista_usuario.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_superuser=False)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            )
        return queryset

class UsuarioCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor']
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'usuarios/cadastrar_usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Usuário cadastrado com sucesso!")
        return response

class UsuarioUpdateView(AccessRequiredMixin, UpdateView):
    allowed_roles = ['Gestor']
    model = Usuario
    form_class = UsuarioChangeForm
    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cadastro atualizado com sucesso!")
        return response

class UsuarioDeleteView(AccessRequiredMixin, DeleteView):
    allowed_roles = ['Gestor']
    model = Usuario
    template_name = 'usuarios/excluir_usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Usuário excluído com sucesso!")
        return response
