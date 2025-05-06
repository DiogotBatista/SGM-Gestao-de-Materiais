from django import forms
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from .models import MovimentoItem, Movimentacao

class MovimentoItemEntradaForm(forms.ModelForm):
    class Meta:
        model = MovimentoItem
        fields = ['material', 'quantidade']
        labels = {
            'material': 'Material',
            'quantidade': 'Quantidade',
        }
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].required = True
        self.fields['quantidade'].required = True
        self.fields['quantidade'].error_messages = {'required': 'Informe a quantidade para a entrada.'}
        self.fields['quantidade'].error_messages['invalid'] = "Informe um número inteiro válido."

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is None:
            return quantidade
        if quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser um valor positivo.")
        return quantidade

    def save(self, commit=True):
        # Define o tipo de movimentação como "Entrada"
        self.instance.tipo = MovimentoItem.ENTRADA
        return super().save(commit=commit)


class MovimentoItemSaidaForm(forms.ModelForm):
    class Meta:
        model = MovimentoItem
        fields = ['material', 'quantidade']
        labels = {
            'material': 'Material',
            'quantidade': 'Quantidade',
        }
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].required = True
        self.fields['quantidade'].required = True
        self.fields['quantidade'].error_messages = {'required': 'Informe a quantidade para a entrada.'}
        self.fields['quantidade'].error_messages['invalid'] = "Informe um número inteiro válido."

    def save(self, commit=True):
        # Define o tipo de movimentação como "Saída"
        self.instance.tipo = MovimentoItem.SAIDA
        return super().save(commit=commit)


class MovimentacaoEntradaForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['documento', 'observacoes']
        labels = {
            'documento': 'Documento de Origem',
            'observacoes': 'Observações',
        }
        help_texts = {
            'documento': 'Informe o documento de origem, ex: NF, devolução, etc.',
        }
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo "documento" obrigatório para entrada
        self.fields['documento'].required = True
        self.fields['documento'].error_messages = {'required': 'O documento de origem é obrigatório.'}


class MovimentacaoSaidaForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['obra', 'observacoes']
        labels = {
            'obra': 'Obra',
            'observacoes': 'Observações',
        }
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo "obra" obrigatório para saída
        self.fields['obra'].required = True
        self.fields['obra'].error_messages = {'required': 'A obra é obrigatória para a saída.'}
        self.fields['obra'].queryset = self.fields['obra'].queryset.filter(ativo=True)


# Formset customizado para validação de itens de movimentação de saída
class BaseMovimentoItemSaidaFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            # Ignora formulários vazios ou que foram marcados para deleção
            if not form.cleaned_data or form.cleaned_data.get('DELETE', False):
                continue

            quantidade = form.cleaned_data.get('quantidade')
            material = form.cleaned_data.get('material')

            if quantidade is None or material is None:
                continue

            if quantidade <= 0:
                raise forms.ValidationError("A quantidade deve ser um valor positivo.")

            # Valida se o saldo atual do material é suficiente para a saída
            if material.saldo_total < quantidade:
                raise forms.ValidationError(
                    f"Quantidade para saída ({quantidade}) excede o saldo disponível ({material.saldo_total}) para o material {material}."
                )


# Definição do formset de saída utilizando o form customizado e o formset customizado
MovimentoItemSaidaFormSet = inlineformset_factory(
    Movimentacao,
    MovimentoItem,
    form=MovimentoItemSaidaForm,
    formset=BaseMovimentoItemSaidaFormSet,
    extra=1,
    can_delete=False
)
