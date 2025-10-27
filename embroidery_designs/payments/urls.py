from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:design_id>/', views.create_payment, name='create_payment'),
    path('success/', views.payment_success, name='payment_success'),
    path('fail/', views.payment_fail, name='payment_fail'),
]