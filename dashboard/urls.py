from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/sector/<str:ticker>/', views.sector_detail, name='sector_detail'),
]
