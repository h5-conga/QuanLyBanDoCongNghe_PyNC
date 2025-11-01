class User:
    """Lớp đại diện cho Người dùng"""

    def __init__(self, ma_user: str, ten_dang_nhap: str, mat_khau: str,
                 ho_ten: str, email: str, vai_tro: str = "nhanvien",
                 trang_thai: str = "hoatdong"):
        self.ma_user = ma_user
        self.ten_dang_nhap = ten_dang_nhap
        self.mat_khau = mat_khau  # Nên mã hóa trong thực tế
        self.ho_ten = ho_ten
        self.email = email
        self.vai_tro = vai_tro  # admin, quanly, nhanvien
        self.trang_thai = trang_thai  # hoatdong, khoa

    def kiem_tra_mat_khau(self, mat_khau: str) -> bool:
        """Kiểm tra mật khẩu"""
        return self.mat_khau == mat_khau

    def la_admin(self) -> bool:
        """Kiểm tra có phải admin không"""
        return self.vai_tro == "admin"

    def __str__(self):
        return f"User[{self.ten_dang_nhap}] {self.ho_ten} - {self.vai_tro}"