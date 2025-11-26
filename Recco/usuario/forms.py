from datetime import datetime
import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nome completo', required=True)
    phone = forms.CharField(label='Telefone', required=True)
    city = forms.ChoiceField(label='Cidade', choices=Profile.CITY_CHOICES)
    user_type = forms.ChoiceField(label='Tipo de usuário', choices=Profile.USER_TYPE_CHOICES)
    cpf_cnpj = forms.CharField(label='CPF / CNPJ', required=False)
    razao_social = forms.CharField(label='Razão social', required=False)
    birth_date = forms.CharField(label='Data de nascimento', required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa'}))

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name",
            "phone", "city", "user_type", "cpf_cnpj", "razao_social", "birth_date",
            "password1", "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # adiciona classes bootstrap aos widgets
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = (existing + ' form-select').strip()
            else:
                widget.attrs['class'] = (existing + ' form-control').strip()

    def clean_birth_date(self):
        val = self.cleaned_data.get('birth_date')
        if not val:
            return None
        # aceitar formatos dd/mm/yyyy ou dd-mm-yyyy
        val = val.strip()
        for fmt in ('%d/%m/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(val, fmt).date()
            except ValueError:
                continue
        raise ValidationError("Data inválida. Use dd/mm/aaaa")

    def clean_cpf_cnpj(self):
        val = self.cleaned_data.get('cpf_cnpj', '') or ''
        val_digits = re.sub(r'\D', '', val)
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'pf':
            if not val_digits:
                raise ValidationError("CPF obrigatório para Pessoa Física.")
            if len(val_digits) != 11:
                raise ValidationError("CPF deve ter 11 dígitos.")
        elif user_type == 'pj':
            if not val_digits:
                raise ValidationError("CNPJ obrigatório para Pessoa Jurídica.")
            if len(val_digits) != 14:
                raise ValidationError("CNPJ deve ter 14 dígitos.")
        # opcional: armazenar apenas dígitos
        return val_digits

    def clean(self):
        cleaned = super().clean()
        # regras adicionais: razao_social obrigatória para pj
        if cleaned.get('user_type') == 'pj' and not cleaned.get('razao_social'):
            self.add_error('razao_social', 'Razão social obrigatória para Pessoa Jurídica.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        if commit:
            user.save()
        # criar/atualizar profile
        profile_values = {
            'phone': self.cleaned_data.get('phone'),
            'city': self.cleaned_data.get('city'),
            'user_type': self.cleaned_data.get('user_type'),
            'cpf_cnpj': self.cleaned_data.get('cpf_cnpj'),  # já apenas dígitos
            'razao_social': self.cleaned_data.get('razao_social'),
            'birth_date': self.cleaned_data.get('birth_date'),  # já convertido para date ou None
        }
        Profile.objects.update_or_create(user=user, defaults=profile_values)
        return user

# --- Novo: formulário para editar o Profile (usar na view de edição) ---
class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        required=False,
        input_formats=['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d'],
        widget=forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa', 'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['phone', 'city', 'user_type', 'cpf_cnpj', 'razao_social', 'birth_date']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'cpf_cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_cpf_cnpj(self):
        val = self.cleaned_data.get('cpf_cnpj', '') or ''
        val_digits = re.sub(r'\D', '', val)
        user_type = self.cleaned_data.get('user_type') or (self.instance.user.profile.user_type if self.instance and hasattr(self.instance, 'user') else None)
        if user_type == 'pf':
            if not val_digits:
                raise ValidationError("CPF obrigatório para Pessoa Física.")
            if len(val_digits) != 11:
                raise ValidationError("CPF deve ter 11 dígitos.")
        elif user_type == 'pj':
            if not val_digits:
                raise ValidationError("CNPJ obrigatório para Pessoa Jurídica.")
            if len(val_digits) != 14:
                raise ValidationError("CNPJ deve ter 14 dígitos.")
        return val_digits