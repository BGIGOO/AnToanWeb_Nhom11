from django.urls import path
# from django.contrib.auth import views as auth_views  <-- Bỏ dòng này đi, ko dùng view gốc nữa
from phongtro.views import tai_khoan_views

app_name = 'tai_khoan'

urlpatterns = [
    # Trang /quan_ly_tai_khoan/
    path('', tai_khoan_views.quan_ly_tai_khoan_view, name='quan_ly_tai_khoan'),

    # Trang /quan_ly_tai_khoan/doi_mat_khau/
    path('doi_mat_khau/', 
         tai_khoan_views.DoiMatKhauView.as_view(), # Gọi view mới đã có thông báo
         name='doi_mat_khau'),
]