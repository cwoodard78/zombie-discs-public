from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'disc') 
    list_filter = ('timestamp', 'sender', 'receiver')
    search_fields = ('sender__username', 'receiver__username')
