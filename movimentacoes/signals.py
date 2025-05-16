# movimentacoes/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, DecimalField
from materiais.models import Material
from movimentacoes.models import MovimentoItem

@receiver(post_save, sender=MovimentoItem)
@receiver(post_delete, sender=MovimentoItem)
def update_material_quantity(sender, instance, **kwargs):
    material = instance.material
    entradas = material.movimento_itens.filter(tipo=MovimentoItem.ENTRADA).aggregate(
        total=Sum('quantidade', output_field=DecimalField())
    )['total'] or 0
    saidas = material.movimento_itens.filter(tipo=MovimentoItem.SAIDA).aggregate(
        total=Sum('quantidade', output_field=DecimalField())
    )['total'] or 0
    novo_saldo = material.saldo_inicial + entradas - saidas
    Material.objects.filter(pk=material.pk).update(saldo_atual=novo_saldo)

# @receiver(post_save, sender=MovimentoItem)
# def gerar_codigo_movimentacao(sender, instance, **kwargs):
#     movimentacao = instance.movimentacao
#     if not movimentacao.codigo and movimentacao.pk:
#         tipo = instance.tipo
#         prefixo = 'MVE' if tipo == 'ENT' else 'MVS'
#         movimentacao.codigo = f"{prefixo}{str(movimentacao.pk).zfill(10)}"
#         movimentacao.save(update_fields=['codigo'])