from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login

# Hàm user_passes_test cũ không đủ thông minh, chúng ta tự viết
# from django.contrib.auth.decorators import user_passes_test # (Không cần nữa)


def chutro_required(function):
    """
    Decorator (hàng rào) thông minh:
    1. Chưa đăng nhập -> Chuyển đến trang Login.
    2. Đã đăng nhập, sai role (Admin, Khách) -> Trả về 403 Forbidden.
    3. Đã đăng nhập, đúng role (Chủ Trọ) -> Cho vào.
    """
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        
        # 1. Kiểm tra đã đăng nhập chưa
        if not request.user.is_authenticated:
            # Nếu chưa, "đá" về trang Login
            return redirect_to_login(request.get_full_path())
        
        # 2. Nếu đã đăng nhập, kiểm tra vai trò
        if request.user.is_chu_tro:
            # Đúng Role 2 (Chủ Trọ) -> Cho vào
            return function(request, *args, **kwargs)
        else:
            # Sai Role (Role 1 hoặc 3) -> Cấm (403)
            return HttpResponseForbidden("Bạn không có quyền truy cập trang này. (Chỉ dành cho Chủ Trọ)")

    return _wrapped_view