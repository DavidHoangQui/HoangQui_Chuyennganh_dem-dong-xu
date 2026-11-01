import base64
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2

from xu_ly import dem_dong_xu, doc_anh


def hien_thi(nhan, anh_bgr):
    """Đưa ảnh OpenCV lên một Label của Tkinter (thu nhỏ cho vừa khung)."""
    h, w = anh_bgr.shape[:2]
    ti_le = min(420 / w, 320 / h, 1.0)
    anh_nho = cv2.resize(anh_bgr, (int(w * ti_le), int(h * ti_le)))
    _, buf = cv2.imencode(".png", anh_nho)
    anh_tk = tk.PhotoImage(data=base64.b64encode(buf.tobytes()).decode("ascii"))
    nhan.config(image=anh_tk)
    nhan.image = anh_tk          # giữ tham chiếu, nếu không ảnh sẽ biến mất


def chon_anh():
    duong_dan = filedialog.askopenfilename(
        filetypes=[("Ảnh", "*.jpg *.jpeg *.png *.bmp")])
    if not duong_dan:
        return
    try:
        phuong_phap = "hough" if chon_pp.get() == "Hough Circle" else "contour"
        so_xu, ket_qua, _ = dem_dong_xu(duong_dan, phuong_phap)
    except Exception as loi:
        messagebox.showerror("Lỗi", str(loi))
        return
    hien_thi(nhan_goc, doc_anh(duong_dan))
    hien_thi(nhan_kq, ket_qua)
    nhan_tong.config(text=f"Tổng số đồng xu: {so_xu}")


cua_so = tk.Tk()
cua_so.title("Đếm đồng xu")

khung_tren = tk.Frame(cua_so, pady=8)
khung_tren.pack()
tk.Button(khung_tren, text="Chọn ảnh", command=chon_anh).pack(side="left", padx=5)
chon_pp = tk.StringVar(value="Contour")
tk.OptionMenu(khung_tren, chon_pp, "Hough Circle", "Contour").pack(side="left", padx=5)

khung_anh = tk.Frame(cua_so)
khung_anh.pack()
nhan_goc = tk.Label(khung_anh, text="Ảnh gốc")
nhan_goc.pack(side="left", padx=5)
nhan_kq = tk.Label(khung_anh, text="Kết quả")
nhan_kq.pack(side="left", padx=5)

nhan_tong = tk.Label(cua_so, text="Tổng số đồng xu: --", font=("Arial", 16, "bold"), pady=8)
nhan_tong.pack()

cua_so.mainloop()