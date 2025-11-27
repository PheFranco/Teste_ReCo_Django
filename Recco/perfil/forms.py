from datetime import datetime

from django import forms

from usuario.models import Profile

class ProfileForm(forms.ModelForm):
    birth_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa', 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.birth_date:
            self.initial['birth_date'] = self.instance.birth_date.strftime('%d/%m/%Y')

    class Meta:
        model = Profile
        fields = ['phone', 'city', 'user_type', 'cpf_cnpj', 'razao_social', 'birth_date']
        widgets = {
            'user_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'cpf_cnpj': forms.TextInput(attrs={'placeholder': 'CPF ou CNPJ', 'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': '(61) 99999-9999', 'class': 'form-control'}),
        }

    def clean_birth_date(self):
        value = self.cleaned_data.get('birth_date')
        if not value:
            return None
        try:
            return datetime.strptime(value, '%d/%m/%Y').date()
        except ValueError as exc:
            raise forms.ValidationError('Use o formato dd/mm/aaaa.') from exc