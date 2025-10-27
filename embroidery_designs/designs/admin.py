# embroidery_designs/designs/admin.py

# Register your models here.

# from django.contrib import admin
# from .models import Category, Design, Purchase

# @admin.register(Design)
# class DesignAdmin(admin.ModelAdmin):
#     list_display = ['title', 'price', 'category', 'machine_type', 'get_file_extension', 'is_active']
#     list_filter = ['category', 'machine_type', 'is_active']
#     search_fields = ['title', 'description']
#     list_editable = ['price', 'is_active']
    
#     def get_file_extension(self, obj):
#         return obj.get_file_extension()
#     get_file_extension.short_description = 'Формат'

from django.contrib import admin
from .models import Category, Design, Purchase, DesignRating, DesignReview, HoopSize, DesignVariant

@admin.register(HoopSize)
class HoopSizeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'width', 'height']
    list_filter = ['compatible_machines']

@admin.register(DesignVariant)
class DesignVariantAdmin(admin.ModelAdmin):
    list_display = ['design', 'hoop', 'created_at']
    list_filter = ['hoop']

@admin.register(Design)
class DesignAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'category', 'machine_type', 'design_width', 'design_height', 'stitch_count', 'is_active']
    list_filter = ['category', 'machine_type', 'compatible_hoops', 'is_active']
    search_fields = ['title', 'description']
    list_editable = ['price', 'stitch_count', 'is_active']
    filter_horizontal = ['compatible_hoops']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'price', 'category', 'machine_type')
        }),
        ('Размеры и стежки', {
            'fields': ('design_width', 'design_height', 'stitch_count', 'compatible_hoops')
        }),
        ('Файлы', {
            'fields': ('image_preview', 'design_file')
        }),
        ('Дополнительно', {
            'fields': ('is_active',)
        }),
    )
# Остальные admin регистрации...