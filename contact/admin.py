from django.contrib import admin
from .models import ContactMessage, EmailLog

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email", "message")

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ("recipient", "subject", "sent_at", "status")
    list_filter = ("status", "sent_at")
    search_fields = ("recipient", "subject")
