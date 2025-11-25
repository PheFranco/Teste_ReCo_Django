from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from usuario.models import Profile

def index(request):
    return render(request, 'usuario/home.html', {'title': 'Usuário'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Garantir que exista um Profile para este user
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Login realizado com sucesso.")
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'usuario/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da conta.')
    return redirect('usuario:index')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso. Faça login.")
            return redirect('usuario:login')
    else:
        form = RegisterForm()
    return render(request, 'usuario/register.html', {'form': form})