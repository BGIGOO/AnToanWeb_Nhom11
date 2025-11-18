from django.urls import path
from phongtro.views import quan_tri_views

app_name = 'quan_tri'

urlpatterns = [
    # --- Các path cũ ---
    path('bang_dieu_khien/', quan_tri_views.bang_dieu_khien_view, name='bang_dieu_khien'),
    path('', quan_tri_views.bang_dieu_khien_view, name='bang_dieu_khien_goc'),
    
    # --- THÊM 2 URL MỚI ---
    
    # 1. Trang danh sách: /quan_tri_Nhom11@123/quan_ly_chu_tro/
    path('quan_ly_chu_tro/', 
         quan_tri_views.quan_ly_chu_tro_view, 
         name='quan_ly_chu_tro'),
         
    # 2. Trang sửa (ví dụ: /quan_tri_Nhom11@123/sua_chu_tro/5/)
    # <int:pk> có nghĩa là nó chấp nhận một SỐ (id) ở đây
    path('sua_chu_tro/<int:pk>/', 
         quan_tri_views.sua_chu_tro_view, 
         name='sua_chu_tro'),

     # --- MỚI: QUẢN LÝ KHÁCH HÀNG ---
    path('quan_ly_khach_hang/', 
         quan_tri_views.quan_ly_khach_hang_view, 
         name='quan_ly_khach_hang'),
         
    path('sua_khach_hang/<int:pk>/', 
         quan_tri_views.sua_khach_hang_view, 
         name='sua_khach_hang'),
]