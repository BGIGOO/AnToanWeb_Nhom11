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
            "avatar",
            "ngay_sinh",
            "gioi_tinh",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )

class ChuTroRegistrationForm(UserCreationForm):
    """
    Form dùng cho trang đăng ký public (dành cho chủ trọ).
    """
    # Thêm các trường bạn muốn hỏi khi đăng ký
    ho_ten = forms.CharField(max_length=100)
    so_dien_thoai = forms.CharField(max_length=20)

    class Meta(UserCreationForm.Meta):
        model = NguoiDung
        # Chỉ cần hỏi email, password1, password2
        # (ho_ten, so_dien_thoai đã thêm ở trên)
        fields = ("email", "ho_ten", "so_dien_thoai")

    def save(self, commit=True):
        # "Chậm mà chắc": Ghi đè hàm save
        user = super().save(commit=False)
        
        # TỰ ĐỘNG GÁN VAI TRÒ CHỦ TRỌ
        user.vai_tro = NguoiDung.VaiTro.CHU_TRO
        
        # Lấy các trường custom
        user.ho_ten = self.cleaned_data['ho_ten']
        user.so_dien_thoai = self.cleaned_data['so_dien_thoai']
        
        if commit:
            user.save()
        return user