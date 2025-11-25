import re
from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label='Nome completo', required=True)
    phone = forms.CharField(label='Telefone', required=True)
    city = forms.ChoiceField(label='Cidade', choices=Profile.CITY_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # aplicar classes bootstrap/form-control automaticamente
        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.get('class', '')
            if isinstance(widget, forms.Select):
                widget.attrs['class'] = (existing + ' form-select').strip()
            else:
                widget.attrs['class'] = (existing + ' form-control').strip()

# Comandos para rodar o servidor
# cd Recco
# source .venv/bin/activate
# python manage.py runserver 0.0.0.0:8000
# pip install django-widget-tweaks
# reinicie o runserver