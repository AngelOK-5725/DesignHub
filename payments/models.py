from django.db import models

# Create your models here.
# embroidery_designs/payments/models.py

from django.db import models
from django.contrib.auth.models import User
from designs.models import Design
from django.utils import timezone
from django.core.exceptions import ValidationError

class Price(models.Model):
    design = models.OneToOneField(
        'designs.Design',
        on_delete=models.CASCADE,
        related_name='price'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')

    def __str__(self):
        return f"{self.amount} {self.currency}"


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='payment_purchases')
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # цена с учётом скидки
    discount_percent = models.PositiveIntegerField(default=0)       # процент скидки на момент покупки
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} — {self.design} — {self.amount} ({self.discount_percent}%)'


# class Discount(models.Model):
#     design = models.OneToOneField(
#         Design,
#         on_delete=models.CASCADE,
#         related_name='discount')
#     percent = models.PositiveIntegerField()
#     start_date = models.DateTimeField(default=timezone.now)
#     end_date = models.DateTimeField()
#     active = models.BooleanField(default=True)

#     def is_valid(self):
#         now = timezone.now()
#         return self.active and self.start_date <= now <= self.end_date

#     def __str__(self):
#         return f"{self.percent}% off on {self.design.title}"
class Discount(models.Model):
    design = models.OneToOneField(
        'designs.Design',
        on_delete=models.CASCADE,
        related_name='discount'
    )
    percent = models.PositiveIntegerField()
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)

    def clean(self):
        """
        Проверяем:
        1. Если есть активная скидка для этого дизайна, нельзя ставить новую.
        2. Если срок старой скидки истек, деактивируем её автоматически.
        """
        now = timezone.now()

        # Проверяем, есть ли уже скидка для этого дизайна
        try:
            existing_discount = Discount.objects.get(design=self.design)
            if existing_discount.pk != self.pk:
                # Если старая скидка еще активна и её срок не истек — ошибка
                if existing_discount.active and existing_discount.end_date > now:
                    raise ValidationError(
                        f"Для этого дизайна уже есть действующая скидка {existing_discount.percent}% до {existing_discount.end_date}."
                    )
                # Если срок истек — автоматически деактивируем старую скидку
                if existing_discount.end_date <= now:
                    existing_discount.active = False
                    existing_discount.save(update_fields=['active'])
        except Discount.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        # Вызываем clean() перед сохранением
        self.clean()

        # Если скидка уже истекла — деактивируем
        if self.end_date <= timezone.now():
            self.active = False

        super().save(*args, **kwargs)

    def is_valid(self):
        """Проверка, действует ли скидка прямо сейчас"""
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date

    def __str__(self):
        status = "активна" if self.is_valid() else "неактивна"
        return f"{self.percent}% на {self.design.title} ({status})"