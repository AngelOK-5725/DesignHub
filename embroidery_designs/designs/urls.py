# embroidery_designs/designs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.design_list, name='design_list'),
    path('design/<int:design_id>/', views.item_info, name='item_info'),
    path('my-designs/', views.my_designs, name='my_designs'),
    path('download/<int:design_id>/', views.download_design, name='download_design'),
    path('download-full/<int:design_id>/', views.download_design_full, name='download_design_full'),
    path('design/<int:design_id>/rate/', views.rate_design, name='rate_design'),
    path('design/<int:design_id>/stats/', views.get_design_stats, name='design_stats'),
]