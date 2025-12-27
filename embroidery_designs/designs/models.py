# embroidery_designs/designs/models.py

# Create your models here.


# embroidery_designs/designs/models.py

import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_embroidery_file
from django.core.files.storage import FileSystemStorage
# from payments.models import Purchase


class PlusFriendlyStorage(FileSystemStorage):
    def get_valid_name(self, name):
        name = name.strip().replace(' ', '_')
        return name

class HoopSize(models.Model):
    HOOP_CHOICES = [
        ('RE36b', 'RE36b (200×360 мм)'),
        ('RE28b', 'RE28b (200×280 мм)'),
        ('SQ20b', 'SQ20b (200×200 мм)'),
        ('RE20b', 'RE20b (140×200 мм)'),
        ('SQ14b', 'SQ14b (140×140 мм)'),
        ('RE10b', 'RE10b (100×40 мм)'),
        ('ASQ18b', 'ASQ18b (184×184 мм)'),
        ('SQ10e', 'SQ10e (100×100 мм)'),
    ]
    
    code = models.CharField(max_length=10, choices=HOOP_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    width = models.IntegerField(help_text="Ширина в мм")
    height = models.IntegerField(help_text="Высота в мм")
    compatible_machines = models.TextField(help_text="Совместимые модели машин")
    
    def __str__(self):
        return f"{self.code} ({self.width}×{self.height} мм)"
    
    class Meta:
        verbose_name = 'Размер пялец'
        verbose_name_plural = 'Размеры пялец'

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

def upload_to_original(instance, filename):
    lower_name = filename.lower()
    if lower_name.endswith('.jef+'):
        ext = '.jef+'
        name = filename[:-5]
    else:
        ext = os.path.splitext(filename)[1].lower()
        name = os.path.splitext(filename)[0]
    
    new_filename = f"{name}_{uuid.uuid4().hex[:7]}{ext}"
    
    if ext == '.jef+':
        return f"designs/jef_plus_files/{new_filename}"
    else:
        return f"designs/files/{new_filename}"

class Design(models.Model):
    MACHINE_CHOICES = [
        ('janome', 'Janome'),
        ('brother', 'Brother'),
        ('both', 'Both'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    machine_type = models.CharField(max_length=10, choices=MACHINE_CHOICES)
    
    # Размеры дизайна
    design_width = models.IntegerField(help_text="Ширина дизайна в мм", default=100)
    design_height = models.IntegerField(help_text="Высота дизайна в мм", default=100)
    
    # Количество стежков
    stitch_count = models.IntegerField(
        default=0,
        help_text="Общее количество стежков в дизайне"
    )
    
    # Для совместимости со старыми данными
    design_size = models.CharField(
        max_length=100, 
        help_text="Размер дизайна в мм (например: 100x100)",
        blank=True,
        default="100x100"
    )
    
    # Совместимые пяльца
    compatible_hoops = models.ManyToManyField(
        HoopSize, 
        blank=True,
        verbose_name="Совместимые пяльца",
        help_text="Выберите пяльца, для которых подходит этот дизайн"
    )
    
    image_preview = models.ImageField(upload_to='designs/previews/')
    
    plus_storage = PlusFriendlyStorage()

    design_file = models.FileField(
        upload_to=upload_to_original,
        storage=plus_storage,
        validators=[validate_embroidery_file]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Автоматически обновляем design_size
        self.design_size = f"{self.design_width}x{self.design_height}"
        super().save(*args, **kwargs)
        # Обновляем совместимые пяльца
        self.update_compatible_hoops()
    
    def get_compatible_hoops(self):
        """Автоматически определяет совместимые пяльца"""
        if not self.design_width or not self.design_height:
            return HoopSize.objects.none()
        
        compatible = HoopSize.objects.filter(
            width__gte=self.design_width,
            height__gte=self.design_height
        )
        return compatible
    
    def update_compatible_hoops(self):
        """Обновляет список совместимых пялец"""
        auto_compatible = self.get_compatible_hoops()
        self.compatible_hoops.set(auto_compatible)
    
    def get_available_hoops_display(self):
        """Возвращает строку с доступными пяльцами для отображения"""
        hoops = self.compatible_hoops.all()
        if hoops:
            return ", ".join([hoop.code for hoop in hoops])
        return "Не указано"
    
    def get_stitch_count_display(self):
        """Форматирует количество стежков для отображения"""
        if self.stitch_count >= 1000:
            return f"{self.stitch_count:,} стежков".replace(',', ' ')
        return f"{self.stitch_count} стежков"
    
    def get_file_extension(self):
        if self.design_file:
            ext = os.path.splitext(self.design_file.name)[1]
            return ext.upper().replace('.', '')
        return ""
    
    def get_rating_stats(self):
        ratings = DesignRating.objects.filter(design=self)
        if not ratings.exists():
            return {
                'average': 0,
                'count': 0,
                'distribution': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            }
        
        total = ratings.count()
        average = sum(r.rating for r in ratings) / total
        
        distribution = {}
        for i in range(1, 6):
            distribution[i] = ratings.filter(rating=i).count()
        
        return {
            'average': round(average, 1),
            'count': total,
            'distribution': distribution
        }
    
    def get_purchase_count(self):
        from payments.models import Purchase
        return Purchase.objects.filter(design=self).count()

    
    def get_user_rating(self, user):
        if not user.is_authenticated:
            return None
        try:
            return DesignRating.objects.get(user=user, design=self).rating
        except DesignRating.DoesNotExist:
            return None

class DesignVariant(models.Model):
    """
    Модель для вариантов дизайна под разные пяльца
    (если у одного дизайна есть несколько версий под разные размеры)
    """
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='variants')
    hoop = models.ForeignKey(HoopSize, on_delete=models.CASCADE)
    variant_file = models.FileField(
        upload_to='designs/variants/',
        storage=PlusFriendlyStorage(),
        validators=[validate_embroidery_file]
    )
    stitch_count = models.IntegerField(
        default=0,
        help_text="Количество стежков для этого варианта"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['design', 'hoop']
        verbose_name = 'Вариант дизайна'
        verbose_name_plural = 'Варианты дизайнов'
    
    def __str__(self):
        return f"{self.design.title} - {self.hoop.code}"

# Остальные модели (Purchase, DesignRating, DesignReview) остаются без изменений

# class Purchase(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     design = models.ForeignKey(Design, on_delete=models.CASCADE)
#     purchased_at = models.DateTimeField(auto_now_add=True)
#     transaction_id = models.CharField(max_length=100, blank=True)
    
#     class Meta:
#         unique_together = ['user', 'design']
    
#     def __str__(self):
#         return f"{self.user.username} - {self.design.title}"

class DesignRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'design']
        verbose_name = 'Рейтинг дизайна'
        verbose_name_plural = 'Рейтинги дизайнов'

class DesignReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Отзыв о дизайне'
        verbose_name_plural = 'Отзывы о дизайнах'