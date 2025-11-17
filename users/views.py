from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import ChuTroRegistrationForm # Import Form mới

def register_chutro_view(request):
    """
    View cho trang đăng ký Chủ Trọ.
    """
    if request.method == 'POST':
        form = ChuTroRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save() # Lưu user, tự động gán vai trò CHU_TRO
            login(request, user) # Tự động đăng nhập cho user
            # Chuyển đến trạm điều hướng
            return redirect('redirect_after_login') 
    else:
        form = ChuTroRegistrationForm()
        
    return render(request, 'registration/register_chutro.html', {'form': form})