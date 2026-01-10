# embroidery_designs/payments/views.py

# Create your views here.
# payments/views.py

import hashlib
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.conf import settings
from designs.models import Design
from .models import Purchase, Discount
from django.utils import timezone


@login_required
def create_payment(request, design_id):
    design = get_object_or_404(Design, id=design_id, is_active=True)

    # Проверяем, не куплен ли уже дизайн
    if Purchase.objects.filter(user=request.user, design=design).exists():
        return redirect('design_detail', design_id=design_id)

    # Получаем активную скидку
    now = timezone.now()
    active_discounts = design.discounts.filter(active=True, start_date__lte=now, end_date__gte=now)
    discount_percent = max((d.percent for d in active_discounts), default=0)
    
    # Цена с учётом скидки
    amount = design.price * (1 - discount_percent / 100)

    # Генерируем подпись для FreeKassa
    order_id = f"{request.user.id}_{design.id}_{design.created_at.timestamp()}"
    sign_str = f"{settings.FREEMASSKA_MERCHANT_ID}:{amount}:{settings.FREEMASSKA_SECRET_KEY}:{order_id}"
    signature = hashlib.md5(sign_str.encode()).hexdigest()

    context = {
        'design': design,
        'amount': f"{amount:.2f}",
        'discount_percent': discount_percent,
        'order_id': order_id,
        'signature': signature,
        'merchant_id': settings.FREEMASSKA_MERCHANT_ID,
        'user_email': request.user.email,
    }


    return render(request, 'payments/payment.html', context)


@csrf_exempt
def payment_success(request):
    order_id = request.POST.get('MERCHANT_ORDER_ID')
    amount = request.POST.get('AMOUNT')
    sign = request.POST.get('SIGN')

    sign_str = f"{settings.FREEMASSKA_MERCHANT_ID}:{amount}:{settings.FREEMASSKA_SECRET_KEY2}:{order_id}"
    expected_sign = hashlib.md5(sign_str.encode()).hexdigest()

    if sign == expected_sign:
        # Разбираем order_id
        user_id, design_id, _ = order_id.split('_')
        design = get_object_or_404(Design, id=design_id)
        user = get_object_or_404(User, id=user_id)

        # Получаем активную скидку на момент оплаты
        now = timezone.now()
        active_discounts = design.discounts.filter(active=True, start_date__lte=now, end_date__gte=now)
        discount_percent = max((d.percent for d in active_discounts), default=0)
        final_amount = design.price * (1 - discount_percent / 100)

        # Создаём запись о покупке
        Purchase.objects.get_or_create(
            user=user,
            design=design,
            transaction_id=order_id,
            defaults={
                'amount': final_amount,
                'discount_percent': discount_percent,
            }
        )

        return HttpResponse('YES')
    else:
        return HttpResponse('Invalid signature')


@csrf_exempt
def payment_fail(request):
    return render(request, 'payments/payment_fail.html')
