from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages # Dùng để gửi thông báo
from phongtro.forms.quan_tri_forms import ChuTroChangeForm, KhachHangChangeForm

# Import các model và form
from users.models import NguoiDung
# Import form mới theo đường dẫn cấu trúc mới
from phongtro.forms.quan_tri_forms import ChuTroChangeForm

# ---
# Hàm này đã có (để chạy Bảng điều khiển)
# ---
@login_required
def bang_dieu_khien_view(request):
    """
    View cho trang Bảng điều khiển nghiệp vụ.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
    
    return render(request, 'phongtro/quan_tri/bang_dieu_khien.html', {'user': request.user})

# ---
# View MỚI: Danh sách Chủ Trọ
# ---
@login_required
def quan_ly_chu_tro_view(request):
    """
    Hiển thị danh sách tất cả người dùng có vai trò CHU_TRO.
    """
    # Bảo mật: Chỉ Admin mới được vào
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    # Lấy tất cả Chủ Trọ
    ds_chu_tro = NguoiDung.objects.filter(
        vai_tro=NguoiDung.VaiTro.CHU_TRO
    ).order_by('ho_ten')
    
    context = {
        'user': request.user,
        'ds_chu_tro': ds_chu_tro,
    }
    return render(request, 'phongtro/quan_tri/quan_ly_chu_tro.html', context)

# ---
# View MỚI: Sửa thông tin Chủ Trọ
# ---
@login_required
def sua_chu_tro_view(request, pk):
    """
    Sửa thông tin chi tiết của một Chủ Trọ.
    pk là ID của Chủ Trọ.
    """
    # Bảo mật: Chỉ Admin mới được vào
    if not request.user.is_staff :
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
    
    # Bảo mật: Lấy chính xác user là CHU_TRO, nếu không thì 404
    # (Ngăn admin sửa Role 3 hoặc Role 1 khác bằng URL này)
    chu_tro = get_object_or_404(
        NguoiDung, 
        pk=pk, 
        vai_tro=NguoiDung.VaiTro.CHU_TRO
    )

    if request.method == 'POST':
        # Nếu người dùng gửi form (Save)
        form = ChuTroChangeForm(request.POST, instance=chu_tro)
        if form.is_valid():
            form.save()
            # Gửi tin nhắn thành công
            messages.success(request, f"Cập nhật thông tin cho {chu_tro.ho_ten} thành công.")
            # Chuyển về trang danh sách
            return redirect('quan_tri:quan_ly_chu_tro')
    else:
        # Nếu người dùng mới vào trang (GET)
        form = ChuTroChangeForm(instance=chu_tro)

    context = {
        'user': request.user,
        'form': form,
        'chu_tro': chu_tro, # Gửi chu_tro để lấy tên trên header
    }
    return render(request, 'phongtro/quan_tri/sua_chu_tro.html', context)

@login_required
def quan_ly_khach_hang_view(request):
    """
    Hiển thị danh sách tất cả người dùng có vai trò KHACH_HANG.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")

    # Lấy tất cả Khách Hàng
    ds_khach_hang = NguoiDung.objects.filter(
        vai_tro=NguoiDung.VaiTro.KHACH_HANG
    ).order_by('ho_ten')
    
    context = {
        'user': request.user,
        'ds_khach_hang': ds_khach_hang,
    }
    return render(request, 'phongtro/quan_tri/quan_ly_khach_hang.html', context)

@login_required
def sua_khach_hang_view(request, pk):
    """
    Sửa thông tin chi tiết của một Khách Hàng.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền truy cập trang này.")
    
    # Chỉ lấy user là KHACH_HANG
    khach_hang = get_object_or_404(
        NguoiDung, 
        pk=pk, 
        vai_tro=NguoiDung.VaiTro.KHACH_HANG
    )

    if request.method == 'POST':
        form = KhachHangChangeForm(request.POST, instance=khach_hang)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cập nhật khách hàng {khach_hang.ho_ten} thành công.")
            return redirect('quan_tri:quan_ly_khach_hang')
    else:
        form = KhachHangChangeForm(instance=khach_hang)

    context = {
        'user': request.user,
        'form': form,
        'khach_hang': khach_hang,
    }
    return render(request, 'phongtro/quan_tri/sua_khach_hang.html', context)