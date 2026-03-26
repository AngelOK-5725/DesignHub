# embroidery_designs/comments/urls.py

from django.urls import path
from . import views
urlpatterns = [
    path('design/<int:design_id>/comment/', views.add_comment, name='add_comment'),

]