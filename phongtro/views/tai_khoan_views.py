from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from phongtro.forms.tai_khoan_forms import UserProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

@login_required
def quan_ly_tai_khoan_view(request):
    """
    View cho phép user (bất kể role nào) xem và sửa thông tin mình.
    """
    user = request.user

    if request.method == 'POST':
        # request.FILES là bắt buộc để upload ảnh
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật thông tin thành công!")
            return redirect('tai_khoan:quan_ly_tai_khoan')
        else:
            messages.error(request, "Có lỗi xảy ra. Vui lòng kiểm tra lại.")
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'phongtro/tai_khoan/quan_ly_tai_khoan.html', {
        'form': form
    })

class DoiMatKhauView(SuccessMessageMixin, PasswordChangeView):
    """
    Kế thừa PasswordChangeView để xử lý đổi mật khẩu,
    Kế thừa SuccessMessageMixin để tự động gửi thông báo.
    """
    template_name = 'phongtro/tai_khoan/doi_mat_khau.html'
    
    # Sau khi đổi xong thì quay về trang quản lý tài khoản
    success_url = reverse_lazy('tai_khoan:quan_ly_tai_khoan') 
    
    # Nội dung thông báo hiển thị
    success_message = "Đổi mật khẩu thành công! Vui lòng ghi nhớ mật khẩu mới."