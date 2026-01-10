# embroidery_designs/payments/services.py

from decimal import Decimal
from django.utils import timezone
from payments.models import Price, Discount


def get_final_price(design):
    """
    Возвращает словарь с информацией о цене:
    - final_price: цена после скидки
    - discount_percent: процент скидки
    - discount_ends_in: оставшееся время до конца скидки, пропускаем нули
      (например: "2 дн. 3 ч." или "45 мин." или "1 дн. 30 мин.")
    """
    try:
        price = design.price.amount  # Price обязателен
    except Price.DoesNotExist:
        return {
            'final_price': Decimal('0.00'),
            'discount_percent': 0,
            'discount_ends_in': None
        }

    discount_percent = 0
    discount_ends_in = None

    # Проверяем наличие активной скидки
    if hasattr(design, 'discount') and design.discount.is_valid():
        discount_percent = design.discount.percent

        # Вычисляем финальную цену
        final_price = price * (Decimal('100') - Decimal(discount_percent)) / Decimal('100')

        # Вычисляем оставшееся время до конца скидки
        now = timezone.now()
        delta = design.discount.end_date - now
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60

        # Формируем строку, пропуская нули
        parts = []
        if days > 0:
            parts.append(f"{days} дн.")
        if hours > 0:
            parts.append(f"{hours} ч.")
        if minutes > 0:
            parts.append(f"{minutes} мин.")

        discount_ends_in = " ".join(parts) if parts else None
    else:
        final_price = price

    return {
        'final_price': round(final_price, 2),
        'discount_percent': discount_percent,
        'discount_ends_in': discount_ends_in
    }
