from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Cargo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'groups')

    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data.get('groups')
        if commit:
            user.save()
            if group:
                # Converte o objeto Group em uma lista para set()
                user.groups.set([group])
        else:
            # Define _save_m2m para salvar o grupo posteriormente
            self._save_m2m = lambda: user.groups.set([group]) if group else None
        return user


class UsuarioChangeForm(UserChangeForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Cargo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            user_groups = self.instance.groups.all()
            if user_groups.exists():
                # Define o valor inicial usando o dicionário initial
                self.initial['groups'] = user_groups.first().pk

    def save(self, commit=True):
        user = super().save(commit=False)
        group = self.cleaned_data.get('groups')
        if commit:
            user.save()
            if group:
                user.groups.set([group])
        else:
            self._save_m2m = lambda: user.groups.set([group]) if group else None
        return user
