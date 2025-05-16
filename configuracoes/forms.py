from django import forms
from django.forms import DateInput
from .models import Contratante, Contrato, Obra

class ContratanteForm(forms.ModelForm):
    class Meta:
        model = Contratante
        # Inclua somente os campos que você deseja que o usuário preencha.
        fields = ['nome', 'cnpj', 'ativo']
        labels = {
            'nome': 'Empresa',
            'cnpj': 'CNPJ',
        }
        help_texts = {
            'nome': 'Nome do contratante, ex: Empresa X',
            'cnpj': 'CNPJ do contratante',
            'ativo': 'Indica que o contratante será tratado como ativo. Ao invés de exclui-lo, desmarque isso.',
        }
        widgets = {
            'cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00.000.000/0000-00',
                'data-mask': '00.000.000/0000-00'
            }),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se não houver instância (criação), remova o campo "ativo"
        if not self.instance.pk:
            self.fields.pop('ativo')


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['numero', 'contratante', 'ativo']
        labels = {
            'numero': 'Contrato',
            'contratante': 'Contratante',
            'ativo': 'Ativo',
        }
        help_texts = {
            'numero': 'Número do contrato',
            'ativo': 'Indica se o contrato está ativo',
        }
        widgets = {
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se não houver instância (criação), remova o campo "ativo"
        if not self.instance.pk:
            self.fields.pop('ativo')

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['codigo', 'contrato', 'local', 'ativo']
        labels = {
            'codigo': 'Cod. Obra',
            'local': 'Local',
            'contrato': 'Contrato',
            'ativo': 'Ativo',
        }
        help_texts = {
            'codigo': 'Código da obra/serviço',
            'local': 'Local de execução da obra',
            'contrato': 'Informar o contrato da obra',
            'ativo': 'Indica se a obra está ativa',
        }
        widgets = {
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se não houver instância (criação), remova o campo "ativo"
        if not self.instance.pk:
            self.fields.pop('ativo')
        # Customiza o rótulo do campo 'contrato' para exibir também o contratante
        self.fields['contrato'].label_from_instance = lambda obj: f"{obj.numero} - {obj.contratante}"