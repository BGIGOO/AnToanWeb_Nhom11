# Đồ án Web Cho Thuê Phòng Trọ (Django 5.0)

Hướng dẫn cài đặt và chạy dự án cho các thành viên trong nhóm.

## 1. 💻 Cài đặt môi trường (Setup)

### Bước 1: Lấy code
```bash
git clone [https://github.com/BGIGOO/AnToanWeb_Nhom11](https://github.com/BGIGOO/AnToanWeb_Nhom11.git)
cd AnToanWeb_Nhom11
Bước 2: Tạo và kích hoạt môi trường ảo (venv)
Bash

# Tạo môi trường ảo
python -m venv venv

# Kích hoạt venv (trên Windows)
venv\Scripts\activate

# Kích hoạt venv (trên macOS/Linux)
source venv/bin/activate
Bước 3: Cài đặt thư viện
Dự án sử dụng file requirements.txt để quản lý.

Bash

(venv) pip install -r requirements.txt
Bước 4: Cài đặt Cơ sở dữ liệu (MySQL)
Bạn phải có MySQL Server đang chạy trên máy.

Đăng nhập vào MySQL với quyền root.

Chạy các lệnh SQL sau để tạo CSDL và User riêng cho dự án:

SQL

CREATE DATABASE phongtro_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'phongtro_user'@'localhost' IDENTIFIED BY 'mot_mat_khau_bat_ky';

GRANT ALL PRIVILEGES ON phongtro_db.* TO 'phongtro_user'@'localhost';

FLUSH PRIVILEGES;
Bước 5: Cấu hình biến môi trường (.env)
Dự án sử dụng file .env để quản lý bảo mật.

Copy file .env.example thành file .env:

Bash

# (Windows)
copy .env.example .env

# (macOS/Linux)
cp .env.example .env
Mở file .env và điền thông tin CSDL bạn vừa tạo ở Bước 4:

Ini, TOML

# Ví dụ nội dung file .env
SECRET_KEY=thay_bang_mot_chuoi_bi_mat_dai_dai
DATABASE_URL=mysql://phongtro_user:mot_mat_khau_bat_ky@127.0.0.1:3306/phongtro_db
DEBUG=True
2. 🚀 Chạy dự án
Bước 6: "Thi công" CSDL (Migrate)
Lệnh này sẽ tạo tất cả các bảng (User, TinDang...) trong CSDL rỗng của bạn.

Bash

(venv) python manage.py migrate
Bước 7: Nạp dữ liệu mồi (Địa lý)
Lệnh này sẽ tự động tải và nạp hơn 10.000+ Tỉnh/Huyện/Xã của Việt Nam vào CSDL.

Bash

(venv) python manage.py seed_data
Bước 8: Tạo Super Admin (Tài khoản Quản trị)
Bạn cần tài khoản này để truy cập trang /admin.

Bash

(venv) python manage.py createsuperuser
(Sau đó nhập Email, Họ tên, Mật khẩu...)

Bước 9: Chạy server
Bash

(venv) python manage.py runserver
Mở trình duyệt và truy cập http://127.0.0.1:8000/