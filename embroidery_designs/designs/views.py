# embroidery_designs/designs/views.py

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Design, Category, Purchase

from django.http import FileResponse, HttpResponse, JsonResponse
from .forms import RatingForm
from .models import DesignRating

import zipfile
import os
from django.conf import settings

@login_required
def download_design_full(request, design_id):
    """
    Скачивание архива со всеми вариантами дизайна
    """
    design = get_object_or_404(Design, id=design_id)
    
    # Проверяем права на скачивание
    if not Purchase.objects.filter(user=request.user, design=design).exists():
        return HttpResponse("У вас нет прав для скачивания этого файла", status=403)
    
    # Создаем архив в памяти
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{design.title}_full.zip"'
    
    with zipfile.ZipFile(response, 'w') as zip_file:
        # Добавляем основной файл
        if design.design_file:
            file_path = design.design_file.path
            if os.path.exists(file_path):
                arcname = f"{design.title}.{design.get_file_extension().lower()}"
                zip_file.write(file_path, arcname)
        
        # Добавляем варианты для пялец
        for variant in design.variants.all():
            if variant.variant_file:
                variant_path = variant.variant_file.path
                if os.path.exists(variant_path):
                    arcname = f"{design.title}_{variant.hoop.code}.{design.get_file_extension().lower()}"
                    zip_file.write(variant_path, arcname)
    
    return response

@login_required
def download_design(request, design_id):
    """Кастомное скачивание с правильными именами файлов"""
    design = get_object_or_404(Design, id=design_id)
    
    # Проверяем, что пользователь купил этот дизайн
    if not Purchase.objects.filter(user=request.user, design=design).exists():
        return HttpResponse("У вас нет прав для скачивания этого файла", status=403)
    
    response = FileResponse(design.design_file)
    
    # Устанавливаем правильное имя файла
    filename = design.get_download_filename()
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

@login_required
def rate_design(request, design_id):
    """
    Обработка оценки дизайна
    """
    design = get_object_or_404(Design, id=design_id)
    
    if request.method == 'POST':
        rating_value = request.POST.get('rating')
        
        if rating_value and rating_value.isdigit():
            rating_value = int(rating_value)
            
            # Создаем или обновляем рейтинг
            rating, created = DesignRating.objects.get_or_create(
                user=request.user,
                design=design,
                defaults={'rating': rating_value}
            )
            
            if not created:
                rating.rating = rating_value
                rating.save()
            
            # Возвращаем обновленную статистику
            stats = design.get_rating_stats()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'average_rating': stats['average'],
                    'rating_count': stats['count'],
                    'user_rating': rating_value
                })
    
    return redirect('item_info', design_id=design_id)

def get_design_stats(request, design_id):
    """
    API для получения статистики дизайна
    """
    design = get_object_or_404(Design, id=design_id)
    stats = design.get_rating_stats()
    
    return JsonResponse({
        'average_rating': stats['average'],
        'rating_count': stats['count'],
        'purchase_count': design.get_purchase_count()
    })

def design_list(request):
    category_id = request.GET.get('category')
    machine_type = request.GET.get('machine_type')
    search_query = request.GET.get('search')
    page = request.GET.get('page', 1)
    
    designs = Design.objects.filter(is_active=True)
    
    if category_id:
        designs = designs.filter(category_id=category_id)
    
    if machine_type and machine_type != 'both':
        designs = designs.filter(machine_type__in=[machine_type, 'both'])
    
    if search_query:
        designs = designs.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    categories = Category.objects.all()
    
    # Пагинация
    paginator = Paginator(designs, 12)
    designs_page = paginator.get_page(page)
    
    context = {
        'designs': designs_page,
        'categories': categories,
    }
    return render(request, 'designs/all_items.html', context)

def item_info(request, design_id):
    design = get_object_or_404(Design, id=design_id, is_active=True)
    purchased = False
    
    if request.user.is_authenticated:
        purchased = Purchase.objects.filter(
            user=request.user, 
            design=design
        ).exists()
    
    # Похожие дизайны
    similar_designs = Design.objects.filter(
        category=design.category,
        is_active=True
    ).exclude(id=design.id)[:6]
    
    context = {
        'design': design,
        'purchased': purchased,
        'similar_designs': similar_designs,
    }
    return render(request, 'designs/item_info.html', context)

@login_required
def my_designs(request):
    purchases = Purchase.objects.filter(user=request.user).select_related('design')
    designs = [purchase.design for purchase in purchases]
    
    context = {
        'designs': designs,
    }
    return render(request, 'designs/my_designs.html', context)