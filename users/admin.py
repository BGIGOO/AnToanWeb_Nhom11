from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NguoiDung
from .forms import NguoiDungCreationForm, NguoiDungChangeForm

class NguoiDungAdmin(UserAdmin):
    # Gắn form custom vào
    add_form = NguoiDungCreationForm
    form = NguoiDungChangeForm
    model = NguoiDung

    # Các cột trong list view
    list_display = ("email", "ho_ten", "vai_tro", "is_staff", "is_active")
    search_fields = ("email", "ho_ten", "so_dien_thoai")
    list_filter = ("vai_tro", "is_staff", "is_active")

    # Form EDIT (chỉnh sửa user)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Thông tin cá nhân", {
            "fields": ("ho_ten", "so_dien_thoai", "so_zalo",
                       "avatar", "ngay_sinh", "gioi_tinh"),
        }),
        ("Phân quyền", {
            "fields": ("vai_tro", "is_active", "is_staff",
                       "is_superuser", "groups", "user_permissions"),
        }),
        ("Thời gian", {"fields": ("last_login", "date_joined")}),
    )

    # Form ADD (tạo user mới) – chú ý: dùng password1, password2
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "ho_ten",
                "so_dien_thoai",
                "vai_tro",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

    ordering = ("email",)

admin.site.register(NguoiDung, NguoiDungAdmin)
