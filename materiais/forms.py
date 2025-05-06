from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nome', 'unidade', 'grupo', 'armazenagem', 'ativo']
        widgets = {
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se não houver instância (criação), remova o campo "ativo"
        if not self.instance.pk:
            self.fields.pop('ativo')
