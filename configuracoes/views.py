from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from .models import Contratante, Contrato, Obra
from .forms import ContratanteForm, ContratoForm, ObraForm
from usuarios.mixins import AccessRequiredMixin
from django.db.models import Q

class MenuView(AccessRequiredMixin, TemplateView):
    allowed_roles = []
    view_name = 'menu_configuracoes'
    template_name = 'configuracoes/menu.html'

# VIEWS DOS CONTRATANTES
class ContratanteListView(AccessRequiredMixin, ListView):
    allowed_roles = []
    view_name = 'lista_contratantes'
    model = Contratante
    template_name = 'configuracoes/contratantes/lista_contratante.html'
    context_object_name = 'contratantes'
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(cnpj__icontains=query)
            )
        return queryset

class ContratanteCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = []
    view_name = 'criar_contratante'
    no_permission_redirect_url = 'lista_contratantes'
    model = Contratante
    form_class = ContratanteForm
    template_name = 'configuracoes/contratantes/cadastrar_contratante.html'
    success_url = reverse_lazy('lista_contratantes')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Empresa cadastrada com sucesso!")
        return super().form_valid(form)

class ContratanteUpdateView(AccessRequiredMixin, UpdateView):
    allowed_roles = []
    view_name = 'editar_contratante'
    no_permission_redirect_url = 'lista_contratantes'
    model = Contratante
    form_class = ContratanteForm
    template_name = 'configuracoes/contratantes/editar_contratante.html'
    success_url = reverse_lazy('lista_contratantes')

    def form_valid(self, form):
        messages.success(self.request, "Empresa atualizada com sucesso!")
        return super().form_valid(form)

class ContratanteDeleteView(AccessRequiredMixin, DeleteView):
    allowed_roles = []
    view_name = 'deletar_contratante'
    no_permission_redirect_url = 'lista_contratantes'
    model = Contratante
    template_name = 'configuracoes/contratantes/excluir_contratante.html'
    success_url = reverse_lazy('lista_contratantes')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Empresa excluída com sucesso!")
        return response

# VIEWS DOS CONTRATOS
class ContratosListView(AccessRequiredMixin, ListView):
    allowed_roles = []
    view_name = 'lista_contratos'
    model = Contrato
    template_name = 'configuracoes/contratos/lista_contratos.html'
    context_object_name = 'contratos'
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(numero__icontains=query) |
                Q(contratante__nome__icontains=query)
            )
        return queryset

class ContratosCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = []
    view_name = 'criar_contrato'
    no_permission_redirect_url = 'lista_contratos'
    model = Contrato
    form_class = ContratoForm
    template_name = 'configuracoes/contratos/cadastrar_contratos.html'
    success_url = reverse_lazy('lista_contratos')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Contrato cadastrado com sucesso!")
        return super().form_valid(form)

class ContratoUpdateView(AccessRequiredMixin, UpdateView):
    allowed_roles = []
    view_name = 'atualizar_contrato'
    no_permission_redirect_url = 'lista_contratos'
    model = Contrato
    form_class = ContratoForm
    template_name = 'configuracoes/contratos/editar_contratos.html'
    success_url = reverse_lazy('lista_contratos')

    def form_valid(self, form):
        messages.success(self.request, "Contrato atualizado com sucesso!")
        return super().form_valid(form)

class ContratoDeleteView(AccessRequiredMixin, DeleteView):
    allowed_roles = []
    view_name = 'deletar_contrato'
    no_permission_redirect_url = 'lista_contratos'
    model = Contrato
    template_name = 'configuracoes/contratos/excluir_contratos.html'
    success_url = reverse_lazy('lista_contratos')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Contrato excluído com sucesso!")
        return response

# VIEWS DAS OBRAS
class ObrasListView(AccessRequiredMixin, ListView):
    allowed_roles = []
    view_name = 'lista_obras'
    model = Obra
    template_name = 'configuracoes/obras/lista_obras.html'
    context_object_name = 'obras'
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(codigo__icontains=query) |
                Q(contrato__numero__icontains=query)
            )
        return queryset

class ObrasCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = []
    view_name = 'criar_obra'
    no_permission_redirect_url = 'lista_obras'
    model = Obra
    form_class = ObraForm
    template_name = 'configuracoes/obras/cadastrar_obras.html'
    success_url = reverse_lazy('lista_obras')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Obras cadastrada com sucesso!")
        return super().form_valid(form)

class ObrasUpdateView(AccessRequiredMixin, UpdateView):
    allowed_roles = []
    view_name = 'atualizar_obra'
    no_permission_redirect_url = 'lista_obras'
    model = Obra
    form_class = ObraForm
    template_name = 'configuracoes/obras/editar_obras.html'
    success_url = reverse_lazy('lista_obras')

    def form_valid(self, form):
        messages.success(self.request, "Obra atualizada com sucesso!")
        return super().form_valid(form)

class ObrasDeleteView(AccessRequiredMixin, DeleteView):
    allowed_roles = []
    view_name = 'deletar_obra'
    no_permission_redirect_url = 'lista_obras'
    model = Obra
    template_name = 'configuracoes/obras/excluir_obras.html'
    success_url = reverse_lazy('lista_obras')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Obra excluída com sucesso!")
        return response
