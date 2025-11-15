# File: phongtro/management/commands/seed_data.py

import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from phongtro.models import TinhThanh, QuanHuyen, PhuongXa

# URL của file JSON dữ liệu hành chính Việt Nam
DATA_URL = "https://raw.githubusercontent.com/kenzouno1/DiaGioiHanhChinhVN/master/data.json"

class Command(BaseCommand):
    help = 'Nạp dữ liệu Tỉnh/Thành, Quận/Huyện, Phường/Xã từ file JSON'

    @transaction.atomic # Đảm bảo toàn vẹn CSDL, nếu lỗi sẽ rollback
    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("Đang tải dữ liệu từ URL..."))
        
        try:
            response = requests.get(DATA_URL)
            response.raise_for_status() # Báo lỗi nếu request thất bại
            data = response.json()
            #print("JSON received:", data[:1])  # In ra một phần dữ liệu để kiểm tra
            self.stdout.write(self.style.SUCCESS("Tải dữ liệu thành công."))
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Lỗi khi tải dữ liệu: {e}"))
            return

        self.stdout.write("Bắt đầu nạp dữ liệu vào CSDL...")
        
        # Xóa dữ liệu cũ để tránh trùng lặp
        PhuongXa.objects.all().delete()
        QuanHuyen.objects.all().delete()
        TinhThanh.objects.all().delete()

        tinh_count = 0
        huyen_count = 0
        xa_count = 0

        # Bắt đầu vòng lặp
        for tinh_data in data:
            # 1. TỈNH/THÀNH
            tinh, created = TinhThanh.objects.get_or_create(
                ten=tinh_data['Name']  # <-- dùng 'Name' HOA
            )
            tinh_count += 1

            # 2. QUẬN/HUYỆN
            for huyen_data in tinh_data['Districts']:  # <-- 'Districts'
                huyen, created = QuanHuyen.objects.get_or_create(
                    ten=huyen_data['Name'],             # <-- 'Name'
                    tinh_id=tinh
                )
                huyen_count += 1

                # 3. PHƯỜNG/XÃ
                for xa_data in huyen_data['Wards']:    # <-- 'Wards'
                    ten_xa = xa_data.get('Name')       # an toàn hơn
                    if not ten_xa:
                        print("Bỏ qua xa_data không có Name:", xa_data)
                        continue

                    xa, created = PhuongXa.objects.get_or_create(
                        ten=ten_xa,
                        quan_huyen_id=huyen
                    )
                    xa_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f"Hoàn tất! Đã nạp thành công:\n"
            f"- {tinh_count} Tỉnh/Thành\n"
            f"- {huyen_count} Quận/Huyện\n"
            f"- {xa_count} Phường/Xã"
        ))