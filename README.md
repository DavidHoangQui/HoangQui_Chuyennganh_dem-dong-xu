# Nhận dạng và đếm đồng xu trong ảnh

Ứng dụng Python dùng OpenCV để phát hiện và đếm đồng xu trong ảnh.
Hỗ trợ hai phương pháp: **Contour** và **Hough Circle**, có giao diện Tkinter.

## Yêu cầu

- Python 3.9 trở lên
- OpenCV, NumPy

## Cài đặt

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install opencv-python numpy
```

## Cách chạy

Giao diện:
```bash
python gui.py
```

Dòng lệnh:
```bash
python chay.py anh_16xu.jpg contour
python chay.py anh_16xu.jpg hough
```

So sánh hai phương pháp trên nhiều ảnh (sửa danh sách `ANH` trong file trước khi chạy):
```bash
python so_sanh.py
```

## Cấu trúc

| File | Chức năng |
|------|-----------|
| `xu_ly.py` | Xử lý ảnh: đọc ảnh, ảnh xám, tiền xử lý, Hough, Contour |
| `gui.py` | Giao diện Tkinter |
| `chay.py` | Chạy từ dòng lệnh |
| `so_sanh.py` | So sánh kết quả hai phương pháp với số xu thật |
| `thu_tham_so.py` | Thử nhiều bộ tham số Hough |

## Kết quả và hạn chế

- Ảnh các xu rời nhau trên nền sáng: Contour cho kết quả tốt.
- Xu chồng lên nhau mạnh: cả hai phương pháp có thể đếm sai.
- Ảnh một xu lớn chiếm gần hết khung hình: chương trình có thể đếm sai, vì thuật toán được thiết kế cho nhiều xu nhỏ.
- Kết quả Hough có thể khác nhau giữa các phiên bản OpenCV.

## Tác giả

Thang Kim Hoàng Quí - MSSV 110123257