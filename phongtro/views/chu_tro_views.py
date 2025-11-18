from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from phongtro.decorators import chutro_required # Dùng "hàng rào"

# View này CHỈ chứa logic cho Chủ Trọ
@chutro_required # <-- "Hàng rào" cấm Role 1 và 3
@login_required  
def bang_dieu_khien_view(request):
    """
    View cho trang Bảng điều khiển của Chủ trọ (Role 2).
    """
    # Render template ở đường dẫn mới
    return render(request, 'phongtro/chu_tro/bang_dieu_khien.html')