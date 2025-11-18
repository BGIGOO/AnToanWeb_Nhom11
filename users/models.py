import os
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now

# --- HÀM XỬ LÝ ĐỔI TÊN FILE ---
def doi_ten_avatar(instance, filename):
    """
    Hàm này sẽ:
    1. Lấy PK của user (instance.pk).
    2. Lấy thời gian hiện tại.
    3. Tạo tên file mới theo format: avatar_{pk}_{thoigian}.png
    4. Trả về đường dẫn tương đối: avatars/ten_file_moi.png
    """
    
    # Lấy thời gian hiện tại dạng chuỗi 'YYYYMMDDHHMMSS'
    thoi_gian = now().strftime('%Y%m%d%H%M%S')
    
    # Lấy PK. Lưu ý: Khi tạo mới user lần đầu, instance.pk có thể là None.
    # Trong trường hợp đó, ta có thể dùng username hoặc một chuỗi tạm.
    user_id = instance.pk if instance.pk else 'new'
    
    # Tạo tên file mới, LUÔN LÀ .png
    ten_moi = f"avatar_{user_id}_{thoi_gian}.png"
    
    # Trả về đường dẫn: avatars/avatar_1_20231118103000.png
    return os.path.join('avatars', ten_moi)


# ---
# Trình quản lý người dùng (Giữ nguyên code cũ của bạn)
# ---
class NguoiDungManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email là bắt buộc'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('vai_tro', NguoiDung.VaiTro.KHACH_HANG) # Hoặc QUAN_TRI tùy bạn

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser phải có is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser phải có is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# ---
# Model NguoiDung (Cập nhật trường avatar)
# ---
class NguoiDung(AbstractUser):
    
    class VaiTro(models.TextChoices):
        KHACH_HANG = 'KHACH_HANG', _('Khách hàng')
        CHU_TRO = 'CHU_TRO', _('Chủ trọ')
        # QUAN_TRI dùng is_staff=True
    
    class GioiTinh(models.TextChoices):
        NAM = 'nam', _('Nam')
        NU = 'nu', _('Nữ')
        KHAC = 'khac', _('Chưa xác định')

    username = None 
    email = models.EmailField(_('email address'), unique=True)
    ho_ten = models.CharField(_('họ tên'), max_length=100)
    so_dien_thoai = models.CharField(_('số điện thoại'), max_length=20, unique=True)
    so_zalo = models.CharField(_('số Zalo'), max_length=20, blank=True, null=True)
    
    vai_tro = models.CharField(
        max_length=20,
        choices=VaiTro.choices,
        default=VaiTro.KHACH_HANG
    )
    
    # --- CẬP NHẬT TRƯỜNG NÀY ---
    # Thay upload_to='avatars/' bằng hàm 'doi_ten_avatar'
    avatar = models.ImageField(
        _('avatar'),
        upload_to=doi_ten_avatar, 
        blank=True, 
        null=True
    )
    # ---------------------------

    ngay_sinh = models.DateField(blank=True, null=True)
    gioi_tinh = models.CharField(
        max_length=20,
        choices=GioiTinh.choices,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['ho_ten']

    objects = NguoiDungManager()

    def __str__(self):
        return self.email
    
    @property
    def is_khach_hang(self):
        return self.vai_tro == self.VaiTro.KHACH_HANG

    @property
    def is_chu_tro(self):
        return self.vai_tro == self.VaiTro.CHU_TRO