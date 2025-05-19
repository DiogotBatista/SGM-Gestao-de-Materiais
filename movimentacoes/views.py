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
from django.views import View
from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from io import BytesIO
from datetime import datetime
from .utils_google_drive import upload_file_to_drive

class MovimentacoesDashboardView(AccessRequiredMixin, TemplateView):
    allowed_roles = []
    view_name = 'dashboard_movimentacoes'
    template_name = 'movimentacoes/dashboard_movimentacoes.html'

class MovimentoListView(AccessRequiredMixin, ListView):
    allowed_roles = []
    view_name = 'lista_movimentacoes'
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
    view_name = 'detalhe_movimentacao'
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
    allowed_roles = []
    view_name = 'criar_movimentacao_entrada'
    no_permission_redirect_url = 'dashboard_movimentacoes'
    model = Movimentacao
    form_class = MovimentacaoEntradaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_entrada.html'

    def form_valid(self, form):
        form.instance.realizado_por = self.request.user
        self.object = form.save(commit=False)

        material_ids = self.request.POST.getlist('material_id[]')
        quantidades = self.request.POST.getlist('quantidade[]')

        if not material_ids:
            form.add_error(None, "Adicione ao menos um material.")
            return self.form_invalid(form)

        with transaction.atomic():
            self.object.save()

            # Gera o código da movimentação
            if not self.object.codigo:
                prefixo = 'MVE'
                self.object.codigo = f"{prefixo}{str(self.object.pk).zfill(10)}"
                self.object.save(update_fields=['codigo'])

            # Upload da guia digitalizada
            arquivo = self.request.FILES.get('guia_digitalizada')
            if arquivo:
                hoje_str = datetime.now().strftime('%Y%m%d')
                nome = f"guia_{self.object.codigo}_{hoje_str}.pdf"
                link, file_id = upload_file_to_drive(arquivo, nome, replace_file_id=self.object.guia_drive_id)
                self.object.link_guia_digitalizada = link
                self.object.guia_drive_id = file_id
                self.object.save(update_fields=['link_guia_digitalizada', 'guia_drive_id'])

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
        context['materiais_retentos'] = list(zip(
            self.request.POST.getlist('material_id[]'),
            self.request.POST.getlist('quantidade[]'),
            self.request.POST.getlist('material_nome[]')
        ))
        return self.render_to_response(context)

class MovimentacaoSaidaCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = []
    view_name = 'criar_movimentacao_saida'
    no_permission_redirect_url = 'dashboard_movimentacoes'
    model = Movimentacao
    form_class = MovimentacaoSaidaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_saida.html'
    success_url = reverse_lazy('dashboard_movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.realizado_por = self.request.user
        self.object = form.save(commit=False)

        material_ids = self.request.POST.getlist('material_id[]')
        quantidades = self.request.POST.getlist('quantidade[]')

        if not material_ids:
            form.add_error(None, "Adicione ao menos um material.")
            return self.form_invalid(form)

        with transaction.atomic():
            self.object.save()

            # Gera o código da movimentação
            if not self.object.codigo:
                prefixo = 'MVS'
                self.object.codigo = f"{prefixo}{str(self.object.pk).zfill(10)}"
                self.object.save(update_fields=['codigo'])

            # Upload da guia digitalizada
            arquivo = self.request.FILES.get('guia_digitalizada')
            if arquivo:
                hoje_str = datetime.now().strftime('%Y%m%d')
                nome = f"guia_{self.object.codigo}_{hoje_str}.pdf"
                link, file_id = upload_file_to_drive(arquivo, nome, replace_file_id=self.object.guia_drive_id)
                self.object.link_guia_digitalizada = link
                self.object.guia_drive_id = file_id
                self.object.save(update_fields=['link_guia_digitalizada', 'guia_drive_id'])

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
        return redirect('detalhe_movimentacoes', pk=self.object.pk)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['materiais_retentos'] = list(zip(
            self.request.POST.getlist('material_id[]'),
            self.request.POST.getlist('quantidade[]'),
            self.request.POST.getlist('material_nome[]')
        ))
        return self.render_to_response(context)


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

class GuiaMovimentacaoBrancoView(View):
    def get(self, request):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        largura, altura = A4

        topo = altura - 1.2 * cm

        # Nome da empresa
        p.setFont("Helvetica-Bold", 12)
        p.drawCentredString(largura / 2, topo, "CRO - Construtora Ribeiro Oliveira")

        # Título
        p.setFont("Helvetica-Bold", 14)
        p.drawCentredString(largura / 2, topo - 1 * cm, "Guia de Movimentação")

        # Opção Entrada / Saída
        p.setFont("Helvetica", 11)
        p.drawString(2 * cm, topo - 2 * cm, "(  ) Entrada     (  ) Saída")

        # Código e data no sistema
        p.drawString(2 * cm, topo - 3 * cm, "Data do lançamento no sistema: ____/____/________")
        p.drawString(2 * cm, topo - 4 * cm, "Código de lançamento no sistema: ____________________________")

        # Linha separadora
        p.setLineWidth(0.5)
        p.line(2 * cm, topo - 4.5 * cm, largura - 2 * cm, topo - 4.5 * cm)

        # Dados da movimentação
        y = topo - 6 * cm
        p.drawString(2 * cm, y, "Contrato: ____________________________________________")
        y -= 1 * cm
        p.drawString(2 * cm, y, "Obra: _________________________________________________")
        y -= 1 * cm
        p.drawString(2 * cm, y, "Data da movimentação: ____/____/________")

        # Tabela de Itens
        y -= 1 * cm
        p.setFont("Helvetica-Bold", 11)
        p.drawString(2 * cm, y, "Itens:")

        x_ini = 2 * cm
        y -= 0.7 * cm
        colunas = ["Código", "Descrição do Material", "Qtd."]
        larguras = [3.5 * cm, 10.5 * cm, 3.5 * cm]

        p.setFont("Helvetica-Bold", 10)
        for i, titulo in enumerate(colunas):
            p.drawString(x_ini + sum(larguras[:i]), y, titulo)

        y -= 0.3 * cm
        p.line(x_ini, y, x_ini + sum(larguras), y)

        # Linhas de itens
        p.setFont("Helvetica", 10)
        for _ in range(14):
            y -= 0.9 * cm
            p.rect(x_ini, y, larguras[0], 0.8 * cm)
            p.rect(x_ini + larguras[0], y, larguras[1], 0.8 * cm)
            p.rect(x_ini + larguras[0] + larguras[1], y, larguras[2], 0.8 * cm)

        # Assinaturas
        y -= 1 * cm
        p.setFont("Helvetica", 11)
        p.drawString(2 * cm, y, "Responsável pelo envio: ___________________________")
        y -= 1 * cm
        p.drawString(2 * cm, y, "Assinatura: ________________________________________")
        y -= 1.5 * cm
        p.drawString(2 * cm, y, "Responsável pelo recebimento: ______________________")
        y -= 1 * cm
        p.drawString(2 * cm, y, "Assinatura: ________________________________________")

        p.showPage()
        p.save()
        buffer.seek(0)

        filename = f"guia_movimentacao_branco_{datetime.now().strftime('%Y%m%d%H%M')}.pdf"
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response


