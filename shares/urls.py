from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('stock_search', views.stock_search, name='stock_search'),
    path('about', views.about, name='about'),
    path('add_stock.html', views.add_stock, name='add_stock'),
    path('delete_stock.html', views.delete_stock, name='delete_stock'),
    path('delete/<int:stock_id>/', views.delete, name='delete'),
    path('stock/<int:ticker>/', views.stock_detail, name='stock_detail'),

    # path('get_stock_info/', views.get_stock_info, name='get_stock_info'),

    path('stock_detail/', views.stock_detail, name='stock_detail'),
    path('stock_detail/<int:stock_id>/', views.stock_detail, name='stock_detail_with_id'),

]





