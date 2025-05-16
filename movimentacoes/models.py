# movimentacoes/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Movimentacao(models.Model):
    codigo = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        help_text="Código único da movimentação"
    )
    obra = models.ForeignKey(
        'configuracoes.Obra',
        on_delete=models.CASCADE,
        related_name='movimentacoes',
        verbose_name='Obra',
        blank=True,
        null=True
    )
    documento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Doc. de Origem",
        help_text="Informe o documento de origem, ex: NF, devolução, etc."
    )
    data_movimentacao = models.DateTimeField(auto_now_add=True, verbose_name='Data da Movimentação')
    realizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Realizado por'
    )
    responsavel_movimentacao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Responsável pela Liberação/Recebimento",
        help_text="Nome da pessoa que liberou/recebeu o material"
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações gerais')

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
        ordering = ['-data_movimentacao']

    def __str__(self):
        return self.codigo

    @property
    def tipo(self):
        first_item = self.itens.first()
        if first_item:
            return first_item.get_tipo_display()
        return "N/A"


class MovimentoItem(models.Model):
    ENTRADA = 'ENT'
    SAIDA = 'SAI'
    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]
    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name='Movimentação'
    )
    material = models.ForeignKey(
        'materiais.Material',
        on_delete=models.CASCADE,
        related_name='movimento_itens',
        verbose_name='Material'
    )
    tipo = models.CharField(
        max_length=3,
        choices=TIPO_CHOICES,
        verbose_name='Tipo de Movimentação'
    )
    quantidade = models.IntegerField(
       verbose_name='Quantidade'
    )

    class Meta:
        verbose_name = 'Item de Movimentação'
        verbose_name_plural = 'Itens de Movimentação'
        ordering = ['material']

    def clean(self):
        if self.quantidade is None or self.quantidade <= 0:
            raise ValidationError("A quantidade deve ser um valor positivo.")

        if self.tipo == self.SAIDA:
            saldo = self.material.saldo_atual
            if self.quantidade > saldo:
                raise ValidationError(
                    f"Quantidade para saída ({self.quantidade}) excede o saldo disponível ({saldo})."
                )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.quantidade} de {self.material.nome}"