from django.shortcuts import render
from django.http import HttpResponse

# View này CHỈ chứa logic cho Khách (Role 3)
def trang_chu_view(request):
    """
    View cho Trang chủ (Homepage)
    """
    # (Đây là nơi bạn sẽ code trang chủ)
    # Tạm thời trả về 1 dòng text
    return HttpResponse(
        'Đây là Trang Chủ (cho Role 3). <br>'
        '<a href="/accounts/login/">Đăng nhập</a> <br>'
        '<a href="/accounts/register/chu-tro/">Đăng ký Chủ Trọ</a> <br>'
        '<a href="/accounts/register/nguoi-thue/">Đăng ký Người Thuê</a>'
    )