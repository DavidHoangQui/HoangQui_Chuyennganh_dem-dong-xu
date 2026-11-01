# so_sanh.py - So sánh số xu thật với kết quả của Hough và Contour.
# Cách dùng: python so_sanh.py
# Sửa danh sách ANH bên dưới: tên file và số xu bạn đếm bằng tay.
from xu_ly import dem_dong_xu
 
ANH = [
    ("anh_16xu.jpg", 16),
    ("anh 8xu.jpg", 8),      # đổi số 8 thành số xu thật bạn đếm được
    ("anh 20xu.jpg", 20),    # đổi số 20 thành số xu thật bạn đếm được
    ("anh_test.jpg", 16),
]
 
print(f"{'Ảnh':<18}{'Thật':>6}{'Hough':>8}{'Contour':>9}")
print("-" * 41)
for ten, that in ANH:
    try:
        hough, _, _ = dem_dong_xu(ten, "hough")
        contour, _, _ = dem_dong_xu(ten, "contour")
        print(f"{ten:<18}{that:>6}{hough:>8}{contour:>9}")
    except Exception as loi:
        print(f"{ten:<18}  lỗi: {loi}")