from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import UsuarioCreationForm, UsuarioChangeForm
from .mixins import AccessRequiredMixin
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.password_validation import password_validators_help_texts

class UsuarioListView(AccessRequiredMixin, ListView):
    allowed_cargos = []
    view_name = 'lista_usuarios'
    model = User
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
    allowed_cargos = []
    view_name = 'cadastrar_usuario'
    model = User
    form_class = UsuarioCreationForm
    template_name = 'usuarios/cadastrar_usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Usuário cadastrado com sucesso!")
        return response

class UsuarioUpdateView(AccessRequiredMixin, UpdateView):
    allowed_cargos = []
    view_name = 'editar_usuario'
    model = User
    form_class = UsuarioChangeForm
    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Cadastro atualizado com sucesso!")
        return response

class UsuarioDeleteView(AccessRequiredMixin, DeleteView):
    allowed_cargos = []
    view_name = 'excluir_usuario'
    model = User
    template_name = 'usuarios/excluir_usuario.html'
    success_url = reverse_lazy('lista_usuarios')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Usuário excluído com sucesso!")
        return response

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regras_senha'] = password_validators_help_texts()
        return context

