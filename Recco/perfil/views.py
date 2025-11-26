from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from usuario.forms import ProfileForm
from django.contrib.auth.models import User
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

@login_required(login_url='usuario:login')
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            # atualizar campos básicos do User (se vierem no POST)
            fn = request.POST.get('first_name')
            em = request.POST.get('email')
            if fn is not None:
                request.user.first_name = fn
            if em is not None:
                request.user.email = em
            request.user.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect('perfil:index')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        # preenche user fields via contexto
        form = ProfileForm(instance=profile)

    return render(request, 'perfil/edit_profile.html', {
        'form': form,
        'user': request.user,
    })

