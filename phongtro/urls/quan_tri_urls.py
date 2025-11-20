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

    path('quan_ly_tin_dang/', 
         quan_tri_views.quan_ly_tin_dang_view, 
         name='quan_ly_tin_dang'),

    # 2. Trang chi tiết tin: /quan_tri_Nhom11@123/chi_tiet_tin_dang/5/
    path('chi_tiet_tin_dang/<int:pk>/', 
         quan_tri_views.chi_tiet_tin_dang_view, 
         name='chi_tiet_tin_dang'),

    # 3. URL xử lý hành động (Duyệt/Ẩn): Không có giao diện, chỉ xử lý POST
    path('duyet_tin_dang/<int:pk>/', 
         quan_tri_views.duyet_tin_dang_view, 
         name='duyet_tin_dang'),

    path('tin_dang/toggle_hoat_dong/<int:pk>/', 
         quan_tri_views.toggle_hoat_dong_tin_dang_view, 
         name='toggle_hoat_dong'),
         
    # URL cho nút Duyệt Tin (Nếu bạn chưa có)
    path('tin_dang/duyet/<int:pk>/', 
         quan_tri_views.duyet_tin_dang_view, 
         name='duyet_tin_dang'),

    path('quan_ly_bao_cao/', 
         quan_tri_views.quan_ly_bao_cao_view, 
         name='quan_ly_bao_cao'),
         
    # 2. Action xử lý (POST only)
    path('xu_ly_bao_cao/', 
         quan_tri_views.xu_ly_bao_cao_view, 
         name='xu_ly_bao_cao'),
]