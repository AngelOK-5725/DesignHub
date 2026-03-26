from django.contrib import admin

# Register your models here.
# embroidery_designs/comments/admin.py

from django.contrib import admin
from .models import DesignComment

@admin.register(DesignComment)
class DesignCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'design', 'is_verified_purchase', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_verified_purchase', 'created_at']
    list_editable = ['is_active']  # можно скрыть прямо из списка одним кликом
    search_fields = ['user__username', 'design__title', 'text']
    readonly_fields = ['user', 'design', 'text', 'image', 'video', 'is_verified_purchase', 'created_at']