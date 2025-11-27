from django.db import models
from django.conf import settings

class Donation(models.Model):
    CONDITION_CHOICES = [
        ('novo', 'Novo'),
        ('bom', 'Em bom estado'),
        ('ruim', 'Precisa de reparo'),
    ]

    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='bom')
    city = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True, help_text="Email de contato (opcional)")
    contact_phone = models.CharField(max_length=30, blank=True)
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donations')
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='donations/', blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} — {'Disponível' if self.is_available else 'Indisponível'}"

class Message(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Msg from {self.sender} to {self.recipient} on {self.donation}'