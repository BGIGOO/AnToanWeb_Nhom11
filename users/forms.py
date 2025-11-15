from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import NguoiDung

class NguoiDungCreationForm(UserCreationForm):
    """
    Form dùng trong trang Add user của admin.
    Dùng email thay cho username.
    """
    class Meta(UserCreationForm.Meta):
        model = NguoiDung
        # Các field bạn muốn nhập khi tạo mới
        fields = (
            "email",
            "ho_ten",
            "so_dien_thoai",
            "vai_tro",
        )

class NguoiDungChangeForm(UserChangeForm):
    """
    Form dùng trong trang Edit user của admin.
    """
    class Meta:
        model = NguoiDung
        fields = (
            "email",
            "ho_ten",
            "so_dien_thoai",
            "so_zalo",
            "vai_tro",
            "avatar_url",
            "ngay_sinh",
            "gioi_tinh",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )
