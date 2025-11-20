from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages
from django.db.models import Q, Case, When, Value, IntegerField
from django.core.paginator import Paginator # <-- ĐÃ THÊM: Import Paginator

from users.models import NguoiDung
from phongtro.models import TinDang, BaoCao
from phongtro.forms.quan_tri_forms import ChuTroChangeForm
    # from phongtro.forms.quan_tri_forms import KhachHangChangeForm
from phongtro.decorators import quantri_required

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
        # Tái sử dụng ChuTroChangeForm vì logic giống nhau (Sửa thông tin cơ bản)
        # Hoặc dùng KhachHangChangeForm nếu bạn đã tạo riêng
        form = ChuTroChangeForm(request.POST, instance=khach_hang)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cập nhật khách hàng {khach_hang.ho_ten} thành công.")
            return redirect('quan_tri:quan_ly_khach_hang')
    else:
        form = ChuTroChangeForm(instance=khach_hang)

    context = {
        'user': request.user,
        'form': form,
        'khach_hang': khach_hang,
    }
    # Bạn cần tạo template sua_khach_hang.html tương tự sua_chu_tro.html
    # Hoặc dùng chung template nếu muốn tối giản
    return render(request, 'phongtro/quan_tri/sua_khach_hang.html', context)

@quantri_required
def quan_ly_tin_dang_view(request):
    """
    Quản lý toàn bộ tin đăng: Lọc theo từ khóa, trạng thái duyệt, trạng thái hiển thị.
    """
    # SỬA LỖI N+1: Thêm select_related('chu_tro') để tải thông tin chủ trọ ngay lập tức
    ds_tin_dang = TinDang.objects.select_related('chu_tro_id').order_by('-ngay_tao') 

    # --- Lấy tham số lọc MỚI ---
    tim_tieu_de = request.GET.get('tim_tieu_de', '').strip()
    tim_chu_tro = request.GET.get('tim_chu_tro', '').strip()
    tim_dia_chi = request.GET.get('tim_dia_chi', '').strip()
    loc_trang_thai = request.GET.get('loc_trang_thai', '').strip()

    # 1. Lọc theo Tiêu đề
    if tim_tieu_de:
        ds_tin_dang = ds_tin_dang.filter(tieu_de__icontains=tim_tieu_de)

    # 2. Lọc theo Tên chủ trọ
    if tim_chu_tro:
        ds_tin_dang = ds_tin_dang.filter(chu_tro_id__ho_ten__icontains=tim_chu_tro)

    # 3. Lọc theo Địa chỉ (Tìm trong cả địa chỉ chi tiết và tên Quận/Huyện)
    if tim_dia_chi:
        ds_tin_dang = ds_tin_dang.filter(
            Q(dia_chi_chi_tiet__icontains=tim_dia_chi) |
            Q(quan_huyen__ten__icontains=tim_dia_chi) |
            Q(phuong_xa__ten__icontains=tim_dia_chi)
        )

    # 4. Lọc theo Trạng thái Duyệt
    if loc_trang_thai == 'da_duyet':
        ds_tin_dang = ds_tin_dang.filter(trang_thai_duyet=True)
    elif loc_trang_thai == 'cho_duyet':
        ds_tin_dang = ds_tin_dang.filter(trang_thai_duyet=False)

    context = {
        'user': request.user,
        'ds_tin_dang': ds_tin_dang,
        # Truyền lại giá trị lọc để giữ state trên giao diện
        'tim_tieu_de': tim_tieu_de,
        'tim_chu_tro': tim_chu_tro,
        'tim_dia_chi': tim_dia_chi,
        'loc_trang_thai': loc_trang_thai,
    }
    return render(request, 'phongtro/quan_tri/quan_ly_tin_dang.html', context)

@quantri_required
def chi_tiet_tin_dang_view(request, pk):
    """
    Xem chi tiết một tin đăng để quyết định duyệt.
    """
    tin = get_object_or_404(TinDang, pk=pk)
    
    context = {
        'user': request.user,
        'tin': tin,
    }
    return render(request, 'phongtro/quan_tri/chi_tiet_tin_dang.html', context)

@quantri_required
def duyet_tin_dang_view(request, pk):
    """
    Xử lý các nút bấm Duyệt, Gỡ duyệt, Ẩn tin, Hiện tin.
    Chỉ chấp nhận phương thức POST.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    tin = get_object_or_404(TinDang, pk=pk)
    action = request.POST.get('action')

    if action == 'duyet':
        tin.trang_thai_duyet = True
        tin.save()
        messages.success(request, f"Đã duyệt tin: {tin.tieu_de}")
        
    elif action == 'go_duyet':
        tin.trang_thai_duyet = False
        tin.save()
        messages.warning(request, f"Đã gỡ duyệt tin: {tin.tieu_de}")
        
    elif action == 'an_tin':
        tin.hoat_dong = False
        tin.save()
        messages.warning(request, f"Đã ẩn tin: {tin.tieu_de}")
        
    elif action == 'hien_tin':
        tin.hoat_dong = True
        tin.save()
        messages.success(request, f"Đã cho hiện tin: {tin.tieu_de}")

    # Xử lý xong thì quay lại trang chi tiết của tin đó
    return redirect('quan_tri:chi_tiet_tin_dang', pk=pk)

@quantri_required
def toggle_hoat_dong_tin_dang_view(request, pk):
    """
    Toggle trạng thái hoat_dong (Hiện/Ẩn) của tin đăng.
    """
    tin = get_object_or_404(TinDang, pk=pk)

    if request.method == 'POST':
        # Đảo ngược trạng thái hiện tại
        tin.hoat_dong = not tin.hoat_dong
        tin.save()
        
        trang_thai_moi = "đang hiển thị" if tin.hoat_dong else "đã bị ẩn"
        messages.success(request, f"Đã cập nhật tin '{tin.tieu_de}' thành {trang_thai_moi}.")
        
    return redirect('quan_tri:quan_ly_tin_dang')

@quantri_required
def quan_ly_bao_cao_view(request):
    """
    Hiển thị danh sách báo cáo vi phạm với bộ lọc chi tiết, có phân trang và sắp xếp ưu tiên.
    """
    # Eager load để tối ưu query
    ds_bao_cao = BaoCao.objects.select_related('nguoi_bao_cao_id', 'tin_dang_id', 'tin_dang_id__chu_tro_id')

    # --- Lấy tham số lọc MỚI ---
    tim_email = request.GET.get('tim_email', '').strip()
    tim_ho_ten = request.GET.get('tim_ho_ten', '').strip()
    tim_tin_id = request.GET.get('tim_tin_id', '').strip()
    tim_sdt_zalo = request.GET.get('tim_sdt_zalo', '').strip()
    loc_trang_thai = request.GET.get('loc_trang_thai', '').strip()
    page_number = request.GET.get('page') # Lấy tham số trang hiện tại

    # (Các bước lọc giữ nguyên)
    # 1. Lọc theo Email (Tìm trong cả người báo cáo VÀ chủ trọ của tin bị báo)
    if tim_email:
        ds_bao_cao = ds_bao_cao.filter(
            Q(nguoi_bao_cao_id__email__icontains=tim_email) |
            Q(tin_dang_id__chu_tro_id__email__icontains=tim_email)
        )

    # 2. Lọc theo Họ tên (Người báo cáo)
    if tim_ho_ten:
        ds_bao_cao = ds_bao_cao.filter(nguoi_bao_cao_id__ho_ten__icontains=tim_ho_ten)

    # 3. Lọc theo ID tin bị báo cáo
    if tim_tin_id:
        try:
            tin_id = int(tim_tin_id)
            ds_bao_cao = ds_bao_cao.filter(tin_dang_id__pk=tin_id)
        except ValueError:
            pass # Nếu nhập chữ vào ô ID thì bỏ qua

    # 4. Lọc theo SĐT/Zalo (Người báo cáo)
    if tim_sdt_zalo:
        ds_bao_cao = ds_bao_cao.filter(
            Q(nguoi_bao_cao_id__so_dien_thoai__icontains=tim_sdt_zalo) |
            Q(nguoi_bao_cao_id__so_zalo__icontains=tim_sdt_zalo)
        )

    # 5. Lọc theo Trạng thái
    if loc_trang_thai:
        ds_bao_cao = ds_bao_cao.filter(trang_thai=loc_trang_thai)

    # --- ĐÃ CHỈNH SỬA: LOGIC SẮP XẾP ƯU TIÊN THEO TRẠNG THÁI ---
    # Gán số ưu tiên cho từng trạng thái: 1 (Chờ xử lý), 2 (Đã xử lý), 3 (Bỏ qua)
    ds_bao_cao = ds_bao_cao.annotate(
        trang_thai_order=Case(
            When(trang_thai=BaoCao.TrangThai.CHO_XU_LY, then=Value(1)),
            When(trang_thai=BaoCao.TrangThai.DA_XU_LY, then=Value(2)),
            When(trang_thai=BaoCao.TrangThai.BO_QUA, then=Value(3)),
            output_field=IntegerField()
        )
    ).order_by('trang_thai_order', '-ngay_tao') # Sắp xếp theo thứ tự ưu tiên, rồi đến thời gian mới nhất
    # ----------------------------------------------------------------------


    # --- PHÂN TRANG (PAGINATION) ---
    # 6 báo cáo mỗi trang theo yêu cầu
    paginator = Paginator(ds_bao_cao, 6) 

    try:
        page_obj = paginator.page(page_number)
    except Exception:
        # Nếu trang không tồn tại, hiển thị trang đầu tiên
        page_obj = paginator.page(1)
    
    # Ghi đè ds_bao_cao bằng danh sách đã được phân trang của trang hiện tại
    ds_bao_cao = page_obj.object_list
    
    context = {
        'user': request.user,
        'ds_bao_cao': ds_bao_cao, # Danh sách báo cáo của trang hiện tại
        'page_obj': page_obj,     # Đối tượng trang (có thông tin next/prev)
        'paginator': paginator,   # Đối tượng Paginator
        # Truyền lại giá trị form
        'tim_email': tim_email,
        'tim_ho_ten': tim_ho_ten,
        'tim_tin_id': tim_tin_id,
        'tim_sdt_zalo': tim_sdt_zalo,
        'loc_trang_thai': loc_trang_thai,
        'TrangThai': BaoCao.TrangThai, 
    }
    return render(request, 'phongtro/quan_tri/quan_ly_bao_cao.html', context)

# ---
# View MỚI: Xử lý Trạng thái Báo cáo (Action)
# ---
@quantri_required
def xu_ly_bao_cao_view(request):
    """
    Xử lý đổi trạng thái cho 1 hoặc nhiều báo cáo cùng lúc.
    """
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Lấy danh sách ID các báo cáo được chọn (từ checkbox)
    report_ids = request.POST.getlist('report_ids')
    action = request.POST.get('action') # 'cho_xu_ly', 'da_xu_ly', 'bo_qua'

    if not report_ids or not action:
        messages.error(request, "Vui lòng chọn ít nhất một báo cáo và hành động.")
        return redirect('quan_tri:quan_ly_bao_cao')

    # Cập nhật hàng loạt (Bulk Update)
    so_luong = BaoCao.objects.filter(pk__in=report_ids).update(trang_thai=action)
    
    messages.success(request, f"Đã cập nhật trạng thái cho {so_luong} báo cáo.")
    return redirect('quan_tri:quan_ly_bao_cao')