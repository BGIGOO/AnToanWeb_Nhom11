from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import view từ app 'users' và view CHUNG từ 'phongtro'
from phongtro.views import dung_chung_views
from users import views as users_views

urlpatterns = [
    # A. Super Admin (Không đổi)
    path('admin/', admin.site.urls),

    # B. Admin Nghiệp vụ (Role 1) - Dùng tên mới
    path('quan_tri_Nhom11@123/', include('phongtro.urls.quan_tri_urls')),

    # C. Khu vực Chủ Trọ (Role 2) - Dùng tên mới
    path('chu_tro/', include('phongtro.urls.chu_tro_urls')),

    # D. "Trạm Điều Hướng" (Sau khi login)
    path(
        'redirect-after-login/', 
        dung_chung_views.redirect_after_login_view, 
        name='redirect_after_login'
    ),

    # E. Các đường dẫn Auth
    path('accounts/', include('django.contrib.auth.urls')), # (Cho Login, Logout...)
    path(
        'accounts/register/chu-tro/', 
        users_views.register_chutro_view, 
        name='register_chutro'
    ),
    # (Bạn có thể thêm register_nguoithue_view ở đây)

    # F. Trang chủ & Công khai (Role 3) - Phải đặt cuối cùng
    path('', include('phongtro.urls.public_urls')),
    path('quan_ly_tai_khoan/', include('phongtro.urls.tai_khoan_urls')),
]

# --- Phục vụ file media (Đã có từ Bước 1) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)