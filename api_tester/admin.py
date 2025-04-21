from django.contrib import admin
from .models import APIRequest

# Register your models here.

@admin.register(APIRequest)
class APIRequestAdmin(admin.ModelAdmin):
    list_display = ('method', 'url', 'response_status', 'created_at')
    list_filter = ('method', 'response_status')
    search_fields = ('url',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
