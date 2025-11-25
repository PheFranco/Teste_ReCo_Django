from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('pf', 'Pessoa Física'),
        ('pj', 'Empresa/ONG'),
    )

    CITY_CHOICES = (
        ('brasilia', 'Brasília'),
        ('taguatinga', 'Taguatinga'),
        ('ceilandia', 'Ceilândia'),
        ('samambaia', 'Samambaia'),
        ('sobradinho', 'Sobradinho'),
        ('gama', 'Gama'),
        ('planaltina', 'Planaltina'),
        ('aguas_lindas', 'Águas Lindas'),
        ('valparaiso', 'Valparaíso de Goiás'),
        ('novo_gama', 'Novo Gama'),
        ('formosa', 'Formosa'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField("Telefone", max_length=20, blank=True)
    city = models.CharField("Cidade", max_length=50, choices=CITY_CHOICES, blank=True)
    user_type = models.CharField("Tipo de usuário", max_length=2, choices=USER_TYPE_CHOICES, default='pf')
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=30, blank=True)
    razao_social = models.CharField("Razão social", max_length=255, blank=True)
    birth_date = models.DateField("Data de nascimento", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()