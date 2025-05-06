from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from usuarios.mixins import AccessRequiredMixin
from .models import Material, GrupoMaterial
from .forms import MaterialForm
from django.contrib import messages
from django.db.models import Q



class MaterialListView(AccessRequiredMixin, ListView):
    allowed_roles = []
    model = Material
    template_name = 'materiais/lista_material.html'
    context_object_name = 'materiais'
    paginate_by = 20
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(id__icontains=query)
            )
        grupo = self.request.GET.get('grupo')
        if grupo:
            queryset = queryset.filter(grupo__pk=grupo)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grupos'] = GrupoMaterial.objects.filter(ativo=True)
        return context

class MaterialCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor', 'Almoxarife']
    no_permission_redirect_url = 'lista_materiais'
    model = Material
    form_class = MaterialForm
    template_name = 'materiais/cadastrar_material.html'
    success_url = reverse_lazy('lista_materiais')

    def form_valid(self, form):
        # Atribui o usuário logado como criador e também como quem fez a última atualização
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Material cadastrado com sucesso!")
        return response

class MaterialUpdateView(AccessRequiredMixin, UpdateView):
    allowed_roles = ['Gestor', 'Almoxarife']
    no_permission_redirect_url = 'lista_materiais'
    model = Material
    form_class = MaterialForm
    template_name = 'materiais/editar_material.html'
    success_url = reverse_lazy('lista_materiais')

    def form_valid(self, form):
        # Atualiza o campo updated_by com o usuário logado
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Material atualizado com sucesso!")
        return response

class MaterialDeleteView(AccessRequiredMixin, DeleteView):
    allowed_roles = ['Gestor']
    no_permission_redirect_url = 'lista_materiais'
    model = Material
    template_name = 'materiais/excluir_material.html'
    success_url = reverse_lazy('lista_materiais')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Material excluído com sucesso!")
        return response
