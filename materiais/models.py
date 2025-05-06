from django.db import models
from django.conf import settings
from django.db.models import Sum, IntegerField

class Unidade(models.Model):
    unidade = models.CharField(max_length=50, unique=True, help_text="Nome da unidade, ex: Kg")
    descricao = models.CharField(max_length=50, blank=True, null=True, help_text="Ex: Quilograma")
    ativo = models.BooleanField(default=True, help_text="Indica se a unidade está ativa")

    class Meta:
        ordering = ['unidade']
        verbose_name = 'Unidade'
        verbose_name_plural = 'Unidades'

    def __str__(self):
        return self.unidade

class GrupoMaterial(models.Model):
    nome = models.CharField(max_length=100, unique=True, help_text="Nome do grupo, ex: Materiais de Construção")
    ativo = models.BooleanField(default=True, help_text="Indica se o grupo está ativo")

    class Meta:
        ordering = ['nome']
        verbose_name = 'Grupo de Materiais'
        verbose_name_plural = 'Grupos de Materiais'

    def __str__(self):
        return self.nome

class Material(models.Model):
    nome = models.CharField(max_length=200)
    saldo_inicial = models.PositiveIntegerField(default=0)
    saldo_atual = models.PositiveIntegerField(default=0)
    armazenagem = models.CharField(max_length=20, null=True, blank=True, help_text="Local onde o material esta armazenado")
    # Referência para a Unidade cadastrada
    unidade = models.ForeignKey('Unidade', on_delete=models.SET_NULL, null=True, blank=True)
    # Referência para o Grupo de Material
    grupo = models.ForeignKey('GrupoMaterial', on_delete=models.SET_NULL, null=True, blank=True)
    ativo = models.BooleanField(
        default=True,
        help_text="Indica que o material será tratado como ativo. Ao invés de excluir materiais, desmarque isso."
    )
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='materiais_criados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='materiais_atualizados',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'

    def __str__(self):
        return self.nome

    @property
    def saldo_total(self):
        """
        Calcula o saldo total somando o saldo inicial com as entradas e subtraindo as saídas.
        Assume que existe um relacionamento reverso chamado 'movimento_itens'
        apontando para os itens de movimento relacionados ao material.
        """
        entradas = self.movimento_itens.filter(tipo='ENT').aggregate(
            total=Sum('quantidade', output_field=IntegerField())
        )['total'] or 0
        saidas = self.movimento_itens.filter(tipo='SAI').aggregate(
            total=Sum('quantidade', output_field=IntegerField())
        )['total'] or 0
        return self.saldo_inicial + entradas - saidas




