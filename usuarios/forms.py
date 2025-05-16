from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from usuarios.models import UserProfile, Cargo

class UsuarioCreationForm(UserCreationForm):
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        required=True,
        label="Cargo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            cargo = self.cleaned_data.get('cargo')
            UserProfile.objects.create(user=user, cargo=cargo)
        return user

class UsuarioChangeForm(UserChangeForm):
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        required=True,
        label="Cargo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and hasattr(self.instance, 'userprofile'):
            self.fields['cargo'].initial = self.instance.userprofile.cargo

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.cargo = self.cleaned_data['cargo']
            profile.save()
        return user
