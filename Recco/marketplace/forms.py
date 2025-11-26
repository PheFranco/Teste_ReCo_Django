from django import forms
from .models import Donation, Message

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'condition', 'city', 'contact_email', 'contact_phone', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4, 'class':'form-control'}),
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'condition': forms.Select(attrs={'class':'form-select'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class':'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class':'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escreva sua mensagem...'}),
        }