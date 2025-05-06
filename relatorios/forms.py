from django import forms
from configuracoes.models import Obra, Contrato
from materiais.models import Material

class RelatorioObraForm(forms.Form):
    obra = forms.ModelChoiceField(
        queryset=Obra.objects.all(),
        required=True,
        label='Obra',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RelatorioContratoForm(forms.Form):
    contrato = forms.ModelChoiceField(
        queryset=Contrato.objects.all(),
        required=True,
        label='Contrato',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class RelatorioDataForm(forms.Form):
    data_inicio = forms.DateField(
        required=True,
        label='Data Início',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data inicial'})
    )
    data_fim = forms.DateField(
        required=True,
        label='Data Fim',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Data final'})
    )

class RelatorioMaterialForm(forms.Form):
    TIPO_CHOICES = [
        ('', 'Todos os Tipos'),
        ('ENT', 'Entrada'),
        ('SAI', 'Saída'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['material'].label_from_instance = lambda obj: f"{obj.id} - {obj.nome}"

    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        required=True,
        label='Material',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        label='Tipo de Movimentação',
        widget=forms.Select(attrs={'class': 'form-select'})
    )