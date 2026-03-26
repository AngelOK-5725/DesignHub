from django.db import models

from designs.models import Design
from django.contrib.auth.models import User

# Create your models here.
# embroidery_designs/comments/models.py

class DesignComment(models.Model):
    design = models.ForeignKey(
        Design,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='design_comments'
    )
    text = models.TextField(max_length=2000, blank=True, default='')
    
    # Медиафайлы
    image = models.ImageField(
        upload_to='comments/images/',
        blank=True, null=True
    )
    video = models.FileField(
        upload_to='comments/videos/',
        blank=True, null=True
    )
    
    # Флаг — купил ли пользователь этот дизайн на момент комментария
    # Храним отдельно, чтобы значок не исчезал если покупка удалится
    is_verified_purchase = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)  # для постмодерации — скрыть через админку
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий к дизайну'
        verbose_name_plural = 'Комментарии к дизайнам'

    def __str__(self):
        return f'{self.user.username} → {self.design.title}'