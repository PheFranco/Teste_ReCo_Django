from django.shortcuts import render


def index(request):
    return render(request, 'usuario/index.html', {'title': 'Usuário'})


def login_view(request):
    return render(request, 'usuario/login.html', {})


def register_view(request):
    return render(request, 'usuario/register.html', {})
