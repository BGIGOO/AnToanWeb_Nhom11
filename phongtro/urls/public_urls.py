from django.urls import path
from phongtro.views import public_views

# Đặt namespace
app_name = 'public'

urlpatterns = [
    # / (Trang chủ)
    path('', public_views.trang_chu_view, name='trang_chu'),
    
    # Tương lai: /chi_tiet/1/
    # path('chi_tiet/<int:pk>/', public_views.chi_tiet_view, name='chi_tiet'),
]