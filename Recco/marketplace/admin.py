from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('title', 'donor', 'city', 'condition', 'is_available', 'created_at')
    list_filter = ('is_available', 'condition', 'city')
    search_fields = ('title', 'description', 'donor__username', 'contact_email')