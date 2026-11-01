# thu_tham_so.py - Thử nhiều bộ tham số Hough trên một ảnh.
# Cách dùng: python thu_tham_so.py anh_4xu.jpg
import sys
import cv2
from xu_ly import doc_anh, chuyen_xam, tien_xu_ly, phat_hien_hough

anh = doc_anh(sys.argv[1])
xu_ly = tien_xu_ly(chuyen_xam(anh))
print("Phiên bản OpenCV:", cv2.__version__)
for nhay in (45, 50, 55, 60):
    for nguong in (0.55, 0.6, 0.65, 0.7):
        n = len(phat_hien_hough(xu_ly, do_nhay=nhay, nguong_huong=nguong))
        print(f"do_nhay={nhay}  nguong={nguong}  ->  {n} xu")