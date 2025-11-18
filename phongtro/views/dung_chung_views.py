from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# View này xử lý việc điều hướng chung
@login_required 
def redirect_after_login_view(request):
    """
    Đây là "Trạm Điều Hướng" sau khi đăng nhập thành công.
    Đọc vai trò của user và chuyển hướng cho họ.
    """
    
    # Role 1: Admin Nghiệp vụ (is_staff)
    if request.user.is_staff and not request.user.is_superuser:
        # Dùng URL namespace: 'app_name:url_name'
        return redirect('quan_tri:bang_dieu_khien_goc') 

    # Role 2: Chủ trọ
    if request.user.is_chu_tro:
        return redirect('chu_tro:bang_dieu_khien_goc')
    
    # Role 3: Khách hàng (nguoi_thue)
    return redirect('public:trang_chu')