from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from usuarios.mixins import AccessRequiredMixin
from .models import Movimentacao, MovimentoItem
from django.forms import inlineformset_factory
from .forms import (
    MovimentoItemEntradaForm,
    MovimentoItemSaidaForm,
    MovimentacaoSaidaForm,
    MovimentacaoEntradaForm,
    MovimentoItemSaidaFormSet  # Importamos o formset customizado do forms.py
)
from django.http import JsonResponse, HttpResponse
from materiais.models import Material
from django.shortcuts import redirect
from django.http import HttpResponse
from .pdf_utils import generate_movimentacao_pdf


class MovimentacoesDashboardView(AccessRequiredMixin, TemplateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    template_name = 'movimentacoes/dashboard_movimentacoes.html'

class MovimentoListView(AccessRequiredMixin, ListView):
    allowed_roles = []
    model = Movimentacao
    template_name = 'movimentacoes/lista_movimentacoes.html'
    context_object_name = 'movimentacoes'
    paginate_by = 10
    ordering = ['-data_movimentacao']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(obra__codigo__icontains=query) |
                Q(codigo__icontains=query) |
                Q(documento__icontains=query)
            )
        return queryset


class MovimentoDetailView(AccessRequiredMixin, DetailView):
    allowed_roles = []
    model = Movimentacao
    template_name = 'movimentacoes/detalhe_movimentacoes.html'
    context_object_name = 'movimentacao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens_list = self.object.itens.all()  # 'itens' é o related_name definido no MovimentoItem
        paginator = Paginator(itens_list, 10)  # 10 itens por página
        page = self.request.GET.get('page')
        try:
            itens_paginated = paginator.page(page)
        except PageNotAnInteger:
            itens_paginated = paginator.page(1)
        except EmptyPage:
            itens_paginated = paginator.page(paginator.num_pages)
        context['itens_paginated'] = itens_paginated
        return context


# Formset para movimentação de entrada (sem customização adicional)
MovimentoItemEntradaFormSet = inlineformset_factory(
    Movimentacao,
    MovimentoItem,
    form=MovimentoItemEntradaForm,
    extra=1,
    can_delete=False
)

class MovimentacaoEntradaCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    no_permission_redirect_url = 'dashboard_movimentacoes'
    model = Movimentacao
    form_class = MovimentacaoEntradaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_entrada.html'

    def form_valid(self, form):
        form.instance.realizado_por = self.request.user
        self.object = form.save(commit=False)

        # Obtenha os materiais enviados pelo formulário
        material_ids = self.request.POST.getlist('material_id[]')
        quantidades = self.request.POST.getlist('quantidade[]')

        # Verifica se há pelo menos um material
        if not material_ids:
            form.add_error(None, "Adicione ao menos um material.")
            return self.form_invalid(form)

        with transaction.atomic():
            self.object.save()  # Salva a movimentação somente se houver material
            for mat_id, qtde in zip(material_ids, quantidades):
                MovimentoItem.objects.create(
                    movimentacao=self.object,
                    material_id=mat_id,
                    quantidade=qtde,
                    tipo=MovimentoItem.ENTRADA
                )
        messages.success(self.request, "Movimentação de entrada registrada com sucesso.")
        return redirect('detalhe_movimentacoes', pk=self.object.pk)


    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        # Caso haja erros adicionais, eles podem ser tratados aqui
        return self.render_to_response(context)


class MovimentacaoSaidaCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    no_permission_redirect_url = 'dashboard_movimentacoes'
    model = Movimentacao
    form_class = MovimentacaoSaidaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_saida.html'
    success_url = reverse_lazy('dashboard_movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Se não for utilizar formset dinâmico via JavaScript, não precisa incluir formset no contexto.
        return context

    def form_valid(self, form):
        form.instance.realizado_por = self.request.user
        self.object = form.save(commit=False)

        # Verifica se há pelo menos um material selecionado
        material_ids = self.request.POST.getlist('material_id[]')
        quantidades = self.request.POST.getlist('quantidade[]')
        if not material_ids:
            form.add_error(None, "Adicione ao menos um material.")
            return self.form_invalid(form)

        with transaction.atomic():
            self.object.save()
            for mat_id, qtde in zip(material_ids, quantidades):
                try:
                    material = Material.objects.get(id=mat_id)
                except Material.DoesNotExist:
                    form.add_error(None, f"Material com id {mat_id} não encontrado.")
                    return self.form_invalid(form)

                try:
                    qtde_int = int(qtde)
                except ValueError:
                    form.add_error(None, "Quantidade inválida.")
                    return self.form_invalid(form)

                if qtde_int <= 0:
                    form.add_error(None, "A quantidade deve ser um valor positivo.")
                    return self.form_invalid(form)

                if material.saldo_atual < qtde_int:
                    form.add_error(
                        None,
                        f"Quantidade para saída ({qtde_int}) excede o saldo disponível ({material.saldo_atual}) para o material {material.nome}."
                    )
                    return self.form_invalid(form)

                MovimentoItem.objects.create(
                    movimentacao=self.object,
                    material=material,
                    quantidade=qtde_int,
                    tipo=MovimentoItem.SAIDA
                )
        messages.success(self.request, "Movimentação de saída registrada com sucesso.")
        # return super().form_valid(form)
        return redirect('detalhe_movimentacoes', pk=self.object.pk)


    def form_invalid(self, form):
        messages.warning(self.request, "Erro ao processar a movimentação de saída.")
        return self.render_to_response(self.get_context_data(form=form))


# API que pega os materiais cadastrados
def api_materials(request):
    termo = request.GET.get('term', '')
    if termo.isdigit():
        materiais = Material.objects.filter(ativo=True, id=int(termo))
    else:
        materiais = Material.objects.filter(ativo=True, nome__icontains=termo)

    resultados = []
    for material in materiais:
        label_text = f"{material.id} - {material.nome}"
        resultados.append({
            'id': material.id,
            'label': label_text,
            'saldo': material.saldo_atual,  # Retorna o saldo atual
        })
    return JsonResponse(resultados, safe=False)





class MovimentacaoPrintView(DetailView):
    model = Movimentacao
    template_name = 'movimentacoes/imprimir_movimentacao.html'  # Pode ser usado para contextos, mas não é essencial
    context_object_name = 'movimentacao'

    def render_to_response(self, context, **response_kwargs):
        movimentacao = context['movimentacao']
        pdf_file = generate_movimentacao_pdf(movimentacao)
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="movimentacao_{movimentacao.codigo}.pdf"'
        return response

