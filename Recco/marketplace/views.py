from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.db import OperationalError
from django.db.models import Q

from .models import Donation, Message
from .forms import DonationForm, MessageForm


def index(request):
    try:
        donations = Donation.objects.filter(is_available=True)
    except OperationalError:
        donations = []
    return render(request, 'marketplace/index.html', {'donations': donations})


def detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'marketplace/detail.html', {'donation': donation})


@login_required(login_url='usuario:login')
def create(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            messages.success(request, "Anúncio criado com sucesso.")
            return redirect('marketplace:detail', pk=donation.pk)
    else:
        form = DonationForm()
    return render(request, 'marketplace/create.html', {'form': form})


@login_required(login_url='usuario:login')
def contact_donor(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.method == 'POST':
        body = request.POST.get('message', '').strip()
        # tenta enviar email primeiro, se configurado
        try:
            to = donation.contact_email or donation.donor.email
            if to:
                send_mail(f"Interesse na doação: {donation.title}", body, settings.DEFAULT_FROM_EMAIL, [to])
                messages.success(request, "Mensagem enviada por email ao doador.")
                # opcional: também gravar a mensagem localmente
                if request.user != donation.donor:
                    Message.objects.create(donation=donation, sender=request.user, recipient=donation.donor, text=body)
                return redirect('marketplace:chat', pk=donation.pk)
            else:
                raise RuntimeError("Sem contato por email disponível")
        except (BadHeaderError, ConnectionRefusedError, RuntimeError, Exception):
            # fallback: criar mensagem interna e redirecionar ao chat
            if request.user != donation.donor:
                Message.objects.create(donation=donation, sender=request.user, recipient=donation.donor, text=body)
            messages.info(request, "Contato salvo internamente. Abra o chat para continuar a conversa.")
            return redirect('marketplace:chat', pk=donation.pk)
    # GET: render form (ou redireciona ao chat)
    return redirect('marketplace:chat', pk=donation.pk)


@login_required(login_url='usuario:login')
def chat(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    # apenas participantes podem acessar: doador e quem abriu o anúncio
    if request.user != donation.donor and not request.user.is_authenticated:
        return HttpResponseForbidden()
    form = MessageForm()
    return render(request, 'marketplace/chat.html', {'donation': donation, 'form': form})


@login_required(login_url='usuario:login')
def messages_json(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    # restrição: apenas doador e quem iniciou interesse veem o chat
    if request.user != donation.donor and not request.user.is_authenticated:
        return JsonResponse({'error': 'forbidden'}, status=403)
    qs = Message.objects.filter(donation=donation).order_by('created_at')
    data = [{
        'id': m.id,
        'sender': m.sender.username,
        'recipient': m.recipient.username,
        'text': m.text,
        'created_at': m.created_at.isoformat(),
    } for m in qs]
    return JsonResponse({'messages': data})


@login_required(login_url='usuario:login')
def post_message(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    if request.method != 'POST':
        return JsonResponse({'error': 'method'}, status=405)
    text = request.POST.get('text', '').strip()
    if not text:
        return JsonResponse({'error': 'empty'}, status=400)
    # destinatário é o outro usuário na conversa
    recipient = donation.donor if request.user != donation.donor else None
    # se o doador e quem escreve forem os mesmos não permitir mensagem sem destinatário
    if recipient is None:
        return JsonResponse({'error': 'no recipient'}, status=400)
    msg = Message.objects.create(donation=donation, sender=request.user, recipient=recipient, text=text)
    return JsonResponse({'ok': True, 'id': msg.id, 'created_at': msg.created_at.isoformat()})


@login_required(login_url='usuario:login')
def inbox(request):
    # lista conversas do usuário (uma por doação)
    qs = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).select_related('donation', 'sender', 'recipient').order_by('-created_at')
    conversations = {}
    for m in qs:
        key = m.donation.pk
        if key not in conversations:
            other = m.sender if m.sender != request.user else m.recipient
            conversations[key] = {
                'donation': m.donation,
                'other': other,
                'last_message': m,
            }
    return render(request, 'marketplace/chats.html', {'conversations': conversations.values()})
