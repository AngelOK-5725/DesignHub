# embroidery_designs/payments/services.py

from decimal import Decimal
from django.utils import timezone
from payments.models import Price, Discount


def get_final_price(design):
    try:
        price_obj = design.price
        price = price_obj.amount
        currency = price_obj.currency
    except Price.DoesNotExist:
        return {
            'final_price': Decimal('0.00'),
            'discount_percent': 0,
            'discount_ends_in': None,
            'currency': None
        }

    discount_percent = 0
    discount_ends_in = None

    # Проверяем наличие активной скидки
    if hasattr(design, 'discount') and design.discount.is_valid():
        discount_percent = design.discount.percent

        # Финальная цена
        final_price = price * (Decimal('100') - Decimal(discount_percent)) / Decimal('100')

        # Таймер скидки
        now = timezone.now()
        delta = design.discount.end_date - now

        # ❗ защита от отрицательного времени
        total_seconds = int(delta.total_seconds())
        if total_seconds > 0:
            days = total_seconds // 86400
            hours = (total_seconds % 86400) // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            parts = []
            if days > 0:
                parts.append(f"{days} дн.")
            if hours > 0:
                parts.append(f"{hours} ч.")
            if minutes > 0:
                parts.append(f"{minutes} мин.")
            if seconds > 0 and days == 0:  
                # 👈 секунды показываем только если нет дней (чтобы не перегружать)
                parts.append(f"{seconds} сек.")

            discount_ends_in = " ".join(parts) if parts else None
    else:
        final_price = price

    return {
        'final_price': round(final_price, 2),
        'discount_percent': discount_percent,
        'discount_ends_in': discount_ends_in,
        'currency': currency  # 👈 добавили
    }
