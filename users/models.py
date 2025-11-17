# File: users/models.py
# (PHIÊN BẢN ĐẦY ĐỦ VÀ CHÍNH XÁC)

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# ---
# Trình quản lý người dùng, để xử lý việc tạo user bằng email
# ---
class NguoiDungManager(BaseUserManager):
    """
    Trình quản lý (Manager) cho Custom User Model,
    sử dụng email làm trường định danh chính.
    """
    def create_user(self, email, password, **extra_fields):
        """Tạo và lưu một User mới với email và password."""
        if not email:
            raise ValueError(_('Email là bắt buộc'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Tự động băm mật khẩu (Yêu cầu II.2)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Tạo và lưu một SuperUser mới."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # Gán vai trò là 'Khách hàng' mặc định, admin sẽ dùng cờ is_staff
        extra_fields.setdefault('vai_tro', NguoiDung.VaiTro.KHACH_HANG)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser phải có is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser phải có is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# ---
# Đây chính là Bảng NguoiDung của bạn
# ---
class NguoiDung(AbstractUser):
    """
    Model NguoiDung tùy chỉnh, kế thừa từ AbstractUser của Django.
    """
    
    # 1. Định nghĩa VaiTro (thay cho bảng VaiTro riêng)
    class VaiTro(models.TextChoices):
        KHACH_HANG = 'KHACH_HANG', _('Khách hàng')
        CHU_TRO = 'CHU_TRO', _('Chủ trọ')
        # QUAN_TRI sẽ được đại diện bằng cờ `is_staff = True`
    
    # --- ĐÂY LÀ TRƯỜNG GIỚI TÍNH ĐƯỢC THÊM VÀO ---
    class GioiTinh(models.TextChoices):
        NAM = 'nam', _('Nam')
        NU = 'nu', _('Nữ')
        KHAC = 'khac', _('Chưa xác định') # Dùng 'khac' thay cho 'null' để dễ quản lý
    
    # 2. Bỏ trường 'username' mặc định
    username = None 
    
    # 3. Các trường trong thiết kế của bạn
    email = models.EmailField(_('email address'), unique=True)
    ho_ten = models.CharField(_('họ tên'), max_length=100)
    so_dien_thoai = models.CharField(_('số điện thoại'), max_length=20, unique=True)
    so_zalo = models.CharField(_('số Zalo'), max_length=20, blank=True, null=True)
    
    vai_tro = models.CharField(
        max_length=20,
        choices=VaiTro.choices,
        default=VaiTro.KHACH_HANG
    )
    
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/', # Sẽ lưu vào media/avatars/
        blank=True, 
        null=True
    )
    
    ngay_sinh = models.DateField(blank=True, null=True)
    
    # --- TRƯỜNG GIỚI TÍNH ĐÃ ĐƯỢC THÊM CHÍNH XÁC ---
    gioi_tinh = models.CharField(
        max_length=20,
        choices=GioiTinh.choices,
        blank=True, # Cho phép để trống (tương đương 'null(chua xac dinh)')
        null=True   # Cho phép giá trị NULL trong CSDL
    )
    
    # 4. Django đã có sẵn:
    # 'password_hash' -> `password`
    # 'hoat_dong' -> `is_active`
    # 'ngay_tao' -> `date_joined`
    
    # 5. Chỉ định trường đăng nhập
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['ho_ten'] # Các trường bắt buộc khi chạy createsuperuser

    # 6. Gán trình quản lý
    objects = NguoiDungManager()

    def __str__(self):
        return self.email
    
    # 7. Định nghĩa các hàm kiểm tra vai trò cho dễ
    @property
    def is_khach_hang(self):
        return self.vai_tro == self.VaiTro.KHACH_HANG

    @property
    def is_chu_tro(self):
        return self.vai_tro == self.VaiTro.CHU_TRO