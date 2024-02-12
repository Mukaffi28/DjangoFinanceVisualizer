from django.urls import path
from .import views



urlpatterns = [
    path('', views.index, name="index"),
    path('home/', views.home, name="home"),
    path('stock-chart/', views.stock_chart, name='stock_chart'),
    
]
