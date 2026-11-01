import sys
from xu_ly import doc_anh, chuyen_xam, tien_xu_ly, phat_hien_hough, phat_hien_contour

anh = doc_anh(sys.argv[1])
xu_ly = tien_xu_ly(chuyen_xam(anh))
phuong_phap = sys.argv[2] if len(sys.argv) > 2 else "hough"

if phuong_phap == "hough":
    danh_sach = phat_hien_hough(xu_ly)
else:
    danh_sach = phat_hien_contour(xu_ly)

print(f"Phương pháp: {phuong_phap}")
print(f"Tổng số đồng xu: {len(danh_sach)}")