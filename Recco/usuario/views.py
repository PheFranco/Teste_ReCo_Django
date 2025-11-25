from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def index(request):
    return render(request, 'usuario/home.html', {'title': 'Usuário'})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login realizado com sucesso.')
            # priorizar next se fornecido
            next_url = request.POST.get('next') or request.GET.get('next') or 'usuario:index'
            return redirect(next_url)
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'usuario/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da conta.')
    return redirect('usuario:index')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso. Faça login.')
            return redirect('usuario:login')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = UserCreationForm()
    return render(request, 'usuario/register.html', {'form': form})