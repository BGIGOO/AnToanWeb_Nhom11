from django.urls import path
from phongtro.views import chu_tro_views

# Đặt namespace
app_name = 'chu_tro'

urlpatterns = [
    # /chu_tro/bang_dieu_khien/
    path('bang_dieu_khien/', chu_tro_views.bang_dieu_khien_view, name='bang_dieu_khien'),

    # /chu_tro/
    path('', chu_tro_views.bang_dieu_khien_view, name='bang_dieu_khien_goc'),
]