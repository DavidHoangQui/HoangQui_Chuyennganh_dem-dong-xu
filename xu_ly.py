import cv2
import numpy as np


def doc_anh(duong_dan):
    """Đọc ảnh màu (BGR). Dùng np.fromfile để hỗ trợ đường dẫn có tiếng Việt."""
    du_lieu = np.fromfile(duong_dan, dtype=np.uint8)
    anh = cv2.imdecode(du_lieu, cv2.IMREAD_COLOR)
    if anh is None:
        raise ValueError(f"Không đọc được ảnh: {duong_dan}")
    return anh


def chuyen_xam(anh_mau):
    """Chuyển ảnh màu sang ảnh xám."""
    return cv2.cvtColor(anh_mau, cv2.COLOR_BGR2GRAY)


def tien_xu_ly(anh_xam):
    """Cân bằng sáng (CLAHE), khử nhiễu hạt (Median), làm mịn (Gaussian)."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    can_bang = clahe.apply(anh_xam)
    khu_nhieu = cv2.medianBlur(can_bang, 5)
    return cv2.GaussianBlur(khu_nhieu, (7, 7), 0)


def tao_ban_do_bien(anh_xu_ly):
    """Ảnh biên Canny, giãn nhẹ để chịu được sai lệch 1-2 pixel."""
    bien = cv2.Canny(anh_xu_ly, 40, 120)
    return cv2.dilate(bien, np.ones((3, 3), np.uint8), iterations=1)


def diem_huong_xuyen_tam(gx, gy, do_lon, x, y, r, so_diem=90):
    """
    Tỷ lệ điểm trên chu vi đường tròn có biên 'đúng hướng'.
    Với đường viền thật của đồng xu, gradient (hướng sáng-tối) vuông góc
    với chu vi, tức là hướng xuyên tâm. Chữ khắc và hoa văn thì hướng lộn xộn,
    nên bị loại ở bước này.
    """
    h, w = do_lon.shape[:2]
    goc = np.linspace(0, 2 * np.pi, so_diem, endpoint=False)
    xs = np.round(x + r * np.cos(goc)).astype(int)
    ys = np.round(y + r * np.sin(goc)).astype(int)
    hop_le = (xs >= 0) & (xs < w) & (ys >= 0) & (ys < h)
    if hop_le.sum() < 0.5 * so_diem:
        return 0.0
    xs, ys, goc = xs[hop_le], ys[hop_le], goc[hop_le]

    do_lon_diem = do_lon[ys, xs]
    manh = do_lon_diem > np.percentile(do_lon, 80)   # chỉ xét điểm có biên đủ mạnh
    if not manh.any():
        return 0.0
    ux = gx[ys, xs] / (do_lon_diem + 1e-6)
    uy = gy[ys, xs] / (do_lon_diem + 1e-6)
    cung_huong = np.abs(ux * np.cos(goc) + uy * np.sin(goc)) > 0.8
    return float((manh & cung_huong).sum()) / so_diem


def phat_hien_hough(anh_xu_ly, do_nhay=55, nguong_huong=0.65):
    """
    Tìm đường tròn bằng Hough, chấm điểm từng đường tròn theo hướng biên,
    rồi giữ các đường tròn có điểm cao nhất và không trùng nhau.
    """
    h, w = anh_xu_ly.shape[:2]
    canh_ngan = min(h, w)
    r_min = max(8, int(canh_ngan * 0.02))
    r_max = max(r_min + 1, int(canh_ngan * 0.20))

    cac_duong_tron = cv2.HoughCircles(
        anh_xu_ly, cv2.HOUGH_GRADIENT, dp=1.2,
        minDist=max(10, int(r_min * 1.6)),
        param1=100, param2=do_nhay,
        minRadius=r_min, maxRadius=r_max,
    )
    if cac_duong_tron is None:
        return []

    gx = cv2.Sobel(anh_xu_ly, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(anh_xu_ly, cv2.CV_32F, 0, 1, ksize=3)
    do_lon = np.hypot(gx, gy)

    ung_vien = []
    for x, y, r in np.round(cac_duong_tron[0][:300]).astype(int):
        diem = diem_huong_xuyen_tam(gx, gy, do_lon, x, y, r)
        if diem >= nguong_huong:
            ung_vien.append((diem, int(x), int(y), int(r)))

    # Xét đường tròn có điểm cao trước, bỏ những đường tròn trùng với đường đã giữ
    ung_vien.sort(reverse=True)
    giu_lai = []
    for diem, x, y, r in ung_vien:
        if all(np.hypot(x - k[1], y - k[2]) >= 0.6 * max(r, k[3]) for k in giu_lai):
            giu_lai.append((diem, x, y, r))
    return [(x, y, r) for _, x, y, r in giu_lai]


def phat_hien_contour(anh_xu_ly, do_tron_toi_thieu=0.7):
    """Tìm contour khép kín quanh từng xu, lọc theo diện tích và độ tròn."""
    h, w = anh_xu_ly.shape[:2]
    ban_do_bien = tao_ban_do_bien(anh_xu_ly)
    nhan = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    ban_do_kin = cv2.morphologyEx(ban_do_bien, cv2.MORPH_CLOSE, nhan, iterations=2)
    contours, _ = cv2.findContours(ban_do_kin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ket_qua = []
    for cnt in contours:
        dien_tich = cv2.contourArea(cnt)
        if dien_tich < 0.0005 * h * w or dien_tich > 0.25 * h * w:
            continue
        chu_vi = cv2.arcLength(cnt, True)
        if chu_vi == 0:
            continue
        do_tron = 4 * np.pi * dien_tich / (chu_vi * chu_vi)
        if do_tron < do_tron_toi_thieu:
            continue
        (cx, cy), r = cv2.minEnclosingCircle(cnt)
        ket_qua.append((int(round(cx)), int(round(cy)), int(round(r))))
    return ket_qua


def ve_ket_qua(anh_mau, danh_sach_xu):
    """Vẽ viền xanh, chấm tâm đỏ, đánh số và ghi tổng số đồng xu lên ảnh."""
    ket = anh_mau.copy()
    for i, (x, y, r) in enumerate(danh_sach_xu, start=1):
        cv2.circle(ket, (x, y), r, (0, 255, 0), 2)
        cv2.circle(ket, (x, y), 3, (0, 0, 255), -1)
        cv2.putText(ket, str(i), (x - 8, y - r - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(ket, f"Total coins: {len(danh_sach_xu)}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2, cv2.LINE_AA)
    return ket


def dem_dong_xu(duong_dan, phuong_phap="hough"):
    """Chạy toàn bộ quy trình. Trả về (số xu, ảnh kết quả, danh sách xu)."""
    anh = doc_anh(duong_dan)
    xu_ly = tien_xu_ly(chuyen_xam(anh))
    if phuong_phap == "hough":
        danh_sach = phat_hien_hough(xu_ly)
    else:
        danh_sach = phat_hien_contour(xu_ly)
    return len(danh_sach), ve_ket_qua(anh, danh_sach), danh_sach