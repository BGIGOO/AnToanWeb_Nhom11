from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# View này CHỈ chứa logic cho Quản Trị
@login_required
def bang_dieu_khien_view(request):
    """
    View cho trang Bảng điều khiển nghiệp vụ.
    """
    # Phân quyền
    if request.user.is_superuser:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
    
     # Chỉ cho phép Admin Nghiệp vụ (is_staff)
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
    
    # Render template ở đường dẫn mới
    return render(request, 'phongtro/quan_tri/bang_dieu_khien.html', {'user': request.user})