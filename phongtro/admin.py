# File: phongtro/admin.py

from django.contrib import admin
from . import models # Import tất cả models từ file models.py

# ---
# CÁCH ĐƠN GIẢN NHẤT (Đăng ký để thấy đã)
# ---
admin.site.register(models.TinhThanh)
admin.site.register(models.QuanHuyen)
admin.site.register(models.PhuongXa)

admin.site.register(models.DanhMuc)
admin.site.register(models.TienIch)
admin.site.register(models.DoiTuong)

admin.site.register(models.TinDang)
admin.site.register(models.AnhTinDang)
admin.site.register(models.BaoCao)
admin.site.register(models.TinYeuThich)

# ---
# Sau này, chúng ta có thể tùy chỉnh từng cái 
# (giống như đã làm với NguoiDungAdmin)
# để chúng hiển thị đẹp hơn. 
# Nhưng hiện tại, như vầy là đủ.
# ---