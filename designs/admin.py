# embroidery_designs/designs/admin.py

# Register your models here.

from django.contrib import admin
from .models import Category, Design, DesignRating, DesignReview, HoopSize, DesignVariant, MachineType

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(MachineType)
class MachineTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

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
    list_display = (
        'title',
        'category',
        'design_width',
        'design_height',
        'stitch_count',
        'is_active'
    )

    list_filter = ('category', 'machine_types', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('stitch_count', 'is_active')
    filter_horizontal = ('compatible_hoops', 'machine_types')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'machine_types')
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
