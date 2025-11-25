from django import forms
from usuario.models import Profile

class ProfileForm(forms.ModelForm):
    birth_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'dd/mm/aaaa'})
    )

    class Meta:
        model = Profile
        fields = ['phone', 'city', 'user_type', 'cpf_cnpj', 'razao_social', 'birth_date']
        widgets = {
            'user_type': forms.Select(),
            'city': forms.Select(),
            'cpf_cnpj': forms.TextInput(attrs={'placeholder': 'CPF ou CNPJ'}),
            'razao_social': forms.TextInput(),
            'phone': forms.TextInput(attrs={'placeholder': '(61) 99999-9999'}),
        }