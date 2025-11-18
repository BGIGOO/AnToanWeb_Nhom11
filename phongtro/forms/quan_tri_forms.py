from django import forms
from users.models import NguoiDung

class ChuTroChangeForm(forms.ModelForm):
    class Meta:
        model = NguoiDung
        fields = [
            'email', 
            'ho_ten', 
            'so_dien_thoai', 
            'so_zalo',
            'ngay_sinh',  # Mới thêm
            'gioi_tinh',  # Mới thêm
            'is_active', 
        ]
        labels = {
            'email': 'Email (Không thể thay đổi)',
            'ho_ten': 'Họ và tên',
            'so_dien_thoai': 'Số điện thoại',
            'so_zalo': 'Số Zalo (Nếu có)',
            'ngay_sinh': 'Ngày sinh', # Label mới
            'gioi_tinh': 'Giới tính', # Label mới
            'is_active': 'Trạng thái hoạt động',
        }
        widgets = {
            # Input type="date" để hiện lịch chọn
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
            
            # Checkbox to hơn một chút
            'is_active': forms.CheckboxInput(attrs={'class': 'h-6 w-6 rounded border-gray-300 text-highlight focus:ring-highlight'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True

class KhachHangChangeForm(forms.ModelForm):
    """
    Form này CHỈ cho Admin sửa thông tin Khách Hàng.
    """
    class Meta:
        model = NguoiDung
        fields = [
            'email', 
            'ho_ten', 
            'so_dien_thoai', 
            'so_zalo',
            'ngay_sinh', 
            'gioi_tinh',
            'is_active', 
        ]
        labels = {
            'email': 'Email (Không thể thay đổi)',
            'ho_ten': 'Họ và tên',
            'so_dien_thoai': 'Số điện thoại',
            'so_zalo': 'Số Zalo',
            'ngay_sinh': 'Ngày sinh',
            'gioi_tinh': 'Giới tính',
            'is_active': 'Trạng thái hoạt động',
        }
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-6 w-6 rounded border-gray-300 text-highlight focus:ring-highlight'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True