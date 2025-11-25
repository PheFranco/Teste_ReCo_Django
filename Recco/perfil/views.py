from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# importar Profile do app usuario
from usuario.models import Profile

@login_required(login_url='usuario:login')
def index(request):
    """
    Mostrar informações de perfil do usuário autenticado.
    Se o Profile não existir, cria um registro padrão.
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'perfil/profile.html', context)

