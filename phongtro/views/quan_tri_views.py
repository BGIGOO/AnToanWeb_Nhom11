from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from phongtro.forms.quan_tri_forms import ChuTroChangeForm, KhachHangChangeForm
from phongtro.decorators import quantri_required
from users.models import NguoiDung

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q

from users.models import NguoiDung
from phongtro.forms.quan_tri_forms import ChuTroChangeForm # Giả sử bạn đã tách KhachHangChangeForm nếu cần
    # from phongtro.forms.quan_tri_forms import KhachHangChangeForm # Uncomment nếu đã có
from phongtro.decorators import quantri_required # Giả sử bạn đã đổi tên decorator

# ---
# Hàm này đã có (để chạy Bảng điều khiển)
# ---
@quantri_required
def bang_dieu_khien_view(request):
    """
    View cho trang Bảng điều khiển nghiệp vụ.
    """
    return render(request, 'phongtro/quan_tri/bang_dieu_khien.html', {'user': request.user})

# ---
# View MỚI: Danh sách Chủ Trọ
# ---
@quantri_required
def quan_ly_chu_tro_view(request):
        """
        Hiển thị danh sách chủ trọ với chức năng tìm kiếm và lọc chi tiết.
        """
        # Lấy danh sách gốc (Chỉ lấy Chủ trọ)
        ds_chu_tro = NguoiDung.objects.filter(vai_tro=NguoiDung.VaiTro.CHU_TRO)

        # Lấy tham số từ URL (GET request)
        tim_ten = request.GET.get('tim_ten', '').strip()
        tim_email = request.GET.get('tim_email', '').strip()
        tim_sdt_zalo = request.GET.get('tim_sdt_zalo', '').strip()
        loc_trang_thai = request.GET.get('loc_trang_thai', '').strip()

        # 1. Lọc theo Tên (chứa từ khóa)
        if tim_ten:
            ds_chu_tro = ds_chu_tro.filter(ho_ten__icontains=tim_ten)

        # 2. Lọc theo Email (chứa từ khóa)
        if tim_email:
            ds_chu_tro = ds_chu_tro.filter(email__icontains=tim_email)

        # 3. Lọc theo SĐT hoặc Zalo (chứa từ khóa)
        if tim_sdt_zalo:
            ds_chu_tro = ds_chu_tro.filter(
                Q(so_dien_thoai__icontains=tim_sdt_zalo) | 
                Q(so_zalo__icontains=tim_sdt_zalo)
            )

        # 4. Lọc theo Trạng thái (True/False)
        if loc_trang_thai:
            if loc_trang_thai == 'active':
                ds_chu_tro = ds_chu_tro.filter(is_active=True)
            elif loc_trang_thai == 'inactive':
                ds_chu_tro = ds_chu_tro.filter(is_active=False)

        # Sắp xếp (Mới nhất lên đầu)
        ds_chu_tro = ds_chu_tro.order_by('-date_joined')

        context = {
            'user': request.user,
            'ds_chu_tro': ds_chu_tro,
            # Truyền lại giá trị để giữ form
            'tim_ten': tim_ten,
            'tim_email': tim_email,
            'tim_sdt_zalo': tim_sdt_zalo,
            'loc_trang_thai': loc_trang_thai,
        }
        return render(request, 'phongtro/quan_tri/quan_ly_chu_tro.html', context)

# ---
# View MỚI: Sửa thông tin Chủ Trọ
# ---
@quantri_required
def sua_chu_tro_view(request, pk):
    """
    Sửa thông tin chi tiết của một Chủ Trọ.
    pk là ID của Chủ Trọ.
    """
    # Bảo mật: Lấy chính xác user là CHU_TRO, nếu không thì 404
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
        'chu_tro': chu_tro, 
    }
    return render(request, 'phongtro/quan_tri/sua_chu_tro.html', context)

# ---
# View MỚI: Danh sách Khách Hàng
# ---
@quantri_required
def quan_ly_khach_hang_view(request):
    """
    Hiển thị danh sách khách hàng với chức năng tìm kiếm và lọc chi tiết.
    """
    # Lấy danh sách gốc (Chỉ lấy Khách Hàng)
    ds_khach_hang = NguoiDung.objects.filter(vai_tro=NguoiDung.VaiTro.KHACH_HANG)

    # Lấy tham số từ URL (GET request)
    tim_ten = request.GET.get('tim_ten', '').strip()
    tim_email = request.GET.get('tim_email', '').strip()
    tim_sdt_zalo = request.GET.get('tim_sdt_zalo', '').strip()
    loc_trang_thai = request.GET.get('loc_trang_thai', '').strip()

    # 1. Lọc theo Tên (chứa từ khóa)
    if tim_ten:
        ds_khach_hang = ds_khach_hang.filter(ho_ten__icontains=tim_ten)

    # 2. Lọc theo Email (chứa từ khóa)
    if tim_email:
        ds_khach_hang = ds_khach_hang.filter(email__icontains=tim_email)

    # 3. Lọc theo SĐT hoặc Zalo (chứa từ khóa)
    if tim_sdt_zalo:
        ds_khach_hang = ds_khach_hang.filter(
            Q(so_dien_thoai__icontains=tim_sdt_zalo) | 
            Q(so_zalo__icontains=tim_sdt_zalo)
        )

    # 4. Lọc theo Trạng thái (True/False)
    if loc_trang_thai:
        if loc_trang_thai == 'active':
            ds_khach_hang = ds_khach_hang.filter(is_active=True)
        elif loc_trang_thai == 'inactive':
            ds_khach_hang = ds_khach_hang.filter(is_active=False)

    # Sắp xếp (Mới nhất lên đầu)
    ds_khach_hang = ds_khach_hang.order_by('-date_joined')

    context = {
        'user': request.user,
        'ds_khach_hang': ds_khach_hang,
        # Truyền lại giá trị để giữ form
        'tim_ten': tim_ten,
        'tim_email': tim_email,
        'tim_sdt_zalo': tim_sdt_zalo,
        'loc_trang_thai': loc_trang_thai,
    }
    return render(request, 'phongtro/quan_tri/quan_ly_khach_hang.html', context)

# ---
# View MỚI: Sửa thông tin Khách Hàng
# ---
@quantri_required
def sua_khach_hang_view(request, pk):
    """
    Sửa thông tin chi tiết của một Khách Hàng.
    """
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