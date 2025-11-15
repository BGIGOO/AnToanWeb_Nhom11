# File: phongtro/models.py

from django.db import models
from django.conf import settings # Dùng để liên kết đến Custom User Model

# ---
# 1. CÁC BẢNG ĐỊA LÝ (Giống hệt thiết kế)
# ---
class TinhThanh(models.Model):
    # Django tự động tạo 'tinh_id' (pk, increment)
    ten = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.ten

class QuanHuyen(models.Model):
    # Django tự động tạo 'quan_huyen_id'
    ten = models.CharField(max_length=100, null=False)
    # Khóa ngoại (Ref) đến TinhThanh
    tinh_id = models.ForeignKey(TinhThanh, on_delete=models.CASCADE)

    def __str__(self):
        return self.ten

class PhuongXa(models.Model):
    # Django tự động tạo 'phuong_xa_id'
    ten = models.CharField(max_length=100, null=False)
    # Khóa ngoại (Ref) đến QuanHuyen
    quan_huyen_id = models.ForeignKey(QuanHuyen, on_delete=models.CASCADE)

    def __str__(self):
        return self.ten

# ---
# 2. CÁC BẢNG DANH MỤC ĐƠN LẺ (Giống hệt thiết kế)
# ---
class DanhMuc(models.Model):
    # 'danh_muc_id'
    ten = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.ten

class TienIch(models.Model):
    # 'tien_ich_id'
    ten = models.CharField(max_length=100, null=False)
    icon_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.ten

class DoiTuong(models.Model):
    # 'doi_tuong_id'
    ten = models.CharField(max_length=100, null=False)
    icon_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.ten
    
class TinDang(models.Model):
    # 'tin_dang_id' sẽ được Django tự động tạo (là 'id')
    
    # === Liên kết ===
    
    # chu_tro_id: Liên kết đến NguoiDung
    # DÙNG settings.AUTH_USER_MODEL là cách chuẩn của Django
    # để liên kết đến Bảng User (vì nó ở app 'users')
    chu_tro_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='tin_dang_cua_chu_tro' # Tên gợi nhớ
    )
    
    # Liên kết đến các bảng Địa lý
    tinh_id = models.ForeignKey(TinhThanh, on_delete=models.SET_NULL, null=True)
    quan_huyen_id = models.ForeignKey(QuanHuyen, on_delete=models.SET_NULL, null=True)
    phuong_xa_id = models.ForeignKey(PhuongXa, on_delete=models.SET_NULL, null=True)
    
    # Liên kết đến DanhMuc
    danh_muc_id = models.ForeignKey(DanhMuc, on_delete=models.SET_NULL, null=True)

    # === Thông tin cơ bản ===
    tieu_de = models.CharField(max_length=255)
    mo_ta = models.TextField(blank=True, null=True)
    dia_chi_chi_tiet = models.CharField(max_length=255)
    
    # === Thông tin giá & diện tích ===
    # decimal(10, 2) -> max_digits=10, decimal_places=2
    gia_moi_thang = models.DecimalField(max_digits=10, decimal_places=2)
    dien_tich_m2 = models.FloatField()

    # === Liên kết Nhiều-Nhiều (N-N) ===
    
    # Đây là cách Django xử lý bảng TienIchTinDang
    # Chúng ta không cần tạo Model TienIchTinDang
    # Django sẽ TỰ ĐỘNG tạo bảng đó cho chúng ta
    tien_ich = models.ManyToManyField(TienIch, blank=True)
    
    # Tương tự cho DoiTuongTinDang
    doi_tuong = models.ManyToManyField(DoiTuong, blank=True)

    # === Trạng thái & Thời gian ===
    trang_thai_duyet = models.BooleanField(default=False)
    hoat_dong = models.BooleanField(default=True)
    
    # ngay_tao (default: `now()`) -> auto_now_add=True
    ngay_tao = models.DateTimeField(auto_now_add=True)
    
    # ngay_cap_nhat -> auto_now=True (tự động cập nhật khi save)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tieu_de
    
class AnhTinDang(models.Model):
    # 'anh_id'
    tin_dang_id = models.ForeignKey(TinDang, on_delete=models.CASCADE, related_name='cac_anh')
    image_url = models.CharField(max_length=255)
    la_anh_dai_dien = models.BooleanField(default=False)

    def __str__(self):
        return f"Ảnh cho: {self.tin_dang_id.tieu_de}"


# Bảng BaoCao (Thiết kế N-1 và N-1)
class BaoCao(models.Model):
    # 'bao_cao_id'
    
    class TrangThai(models.TextChoices):
        CHO_XU_LY = 'cho_xu_ly', 'Chờ xử lý'
        DA_XU_LY = 'da_xu_ly', 'Đã xử lý'
        BO_QUA = 'bo_qua', 'Bỏ qua'

    nguoi_bao_cao_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, # Nếu user bị xóa, vẫn giữ báo cáo
        null=True, 
        related_name='cac_bao_cao'
    )
    tin_dang_id = models.ForeignKey(
        TinDang, 
        on_delete=models.CASCADE, # Nếu tin đăng bị xóa, xóa luôn báo cáo
        related_name='cac_bao_cao'
    )
    ly_do = models.TextField()
    trang_thai = models.CharField(
        max_length=20, 
        choices=TrangThai.choices, 
        default=TrangThai.CHO_XU_LY
    )
    ngay_tao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Báo cáo cho tin: {self.tin_dang_id.tieu_de} bởi {self.nguoi_bao_cao_id.email}"


# Bảng TinYeuThich (Thiết kế N-N *có thêm trường*)
class TinYeuThich(models.Model):
    # Đây là trường hợp chúng ta PHẢI tạo bảng N-N bằng tay
    # vì nó có thêm trường 'ngay_luu'
    
    nguoi_thue_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tin_dang_id = models.ForeignKey(TinDang, on_delete=models.CASCADE)
    ngay_luu = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Thay thế cho 'Indexes { (nguoi_thue_id, tin_dang_id) [pk] }'
        # Đảm bảo một người chỉ có thể "thích" một tin 1 lần
        unique_together = ('nguoi_thue_id', 'tin_dang_id')

    def __str__(self):
        return f"{self.nguoi_thue_id.email} thích {self.tin_dang_id.tieu_de}"