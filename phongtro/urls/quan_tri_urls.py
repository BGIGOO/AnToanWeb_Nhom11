from django.urls import path
from phongtro.views import quan_tri_views

# Đặt namespace (tên định danh) cho nhóm URL này
app_name = 'quan_tri'

urlpatterns = [
    # /quan_tri_Nhom11@123/bang_dieu_khien/
    path('bang_dieu_khien/', quan_tri_views.bang_dieu_khien_view, name='bang_dieu_khien'),
    
    # /quan_tri_Nhom11@123/
    path('', quan_tri_views.bang_dieu_khien_view, name='bang_dieu_khien_goc'),
]