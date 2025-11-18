from django import forms
from users.models import NguoiDung
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = NguoiDung
        fields = [
            'avatar', 
            'email', 
            'ho_ten', 
            'so_dien_thoai', 
            'so_zalo', 
            'ngay_sinh', 
            'gioi_tinh'
        ]
        labels = {
            'avatar': 'Ảnh đại diện',
            'email': 'Email (Không thể đổi)',
            'ho_ten': 'Họ và tên',
            'so_dien_thoai': 'Số điện thoại',
            'so_zalo': 'Số Zalo',
            'ngay_sinh': 'Ngày sinh',
            'gioi_tinh': 'Giới tính',
        }
        widgets = {
            'ngay_sinh': forms.DateInput(attrs={'type': 'date'}),
            # --- SỬA Ở ĐÂY ---
            # Dùng FileInput thường để bỏ giao diện mặc định rườm rà của Django
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100',
                'accept': 'image/*' # Chỉ cho chọn ảnh
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True
        
        for field_name, field in self.fields.items():
            if field_name != 'avatar': 
                field.widget.attrs.update({
                    'class': 'w-full px-4 py-2 border border-secondary rounded-lg focus:outline-none focus:ring-2 focus:ring-highlight'
                })

    def clean_avatar(self):
        """
        Hàm này được gọi tự động khi form.is_valid() chạy.
        Nhiệm vụ: Kiểm tra, resize (nếu cần) và chuyển đổi sang PNG.
        """
        avatar = self.cleaned_data.get('avatar')
        
        if not avatar:
            return avatar

        # Nếu không phải là file mới upload (ví dụ file cũ), trả về nguyên vẹn
        if not hasattr(avatar, 'file'):
            return avatar

        try:
            # 1. Mở ảnh bằng Pillow
            img = Image.open(avatar)
            
            # 2. (Tùy chọn) Convert sang RGB nếu là RGBA/P để tránh lỗi khi lưu JPG, 
            # nhưng vì ta lưu PNG nên giữ RGBA là tốt nhất (hỗ trợ trong suốt).
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            # 3. Lưu ảnh vào bộ nhớ tạm dưới dạng PNG
            output = io.BytesIO()
            img.save(output, format='PNG', quality=100)
            output.seek(0)

            # 4. Tạo đối tượng file mới để thay thế file cũ
            # Đổi tên file ngay tại đây để đảm bảo đuôi là .png
            # Tên gốc không quan trọng vì model sẽ đổi lại, nhưng đuôi .png là CẦN THIẾT
            new_image = InMemoryUploadedFile(
                output,
                'ImageField',
                f"{avatar.name.split('.')[0]}.png", # Đặt tạm tên file với đuôi png
                'image/png',
                sys.getsizeof(output),
                None
            )
            
            return new_image

        except Exception as e:
            # Nếu file lỗi không đọc được
            raise forms.ValidationError("File tải lên không hợp lệ hoặc bị lỗi.")