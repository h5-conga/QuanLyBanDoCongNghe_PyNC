class Order_Detail:
    """Lớp đại diện cho Chi tiết đơn hàng"""

    def __init__(self, ma_sp: str, ten_sp: str, so_luong: int, don_gia: float):
        self.ma_sp = ma_sp
        self.ten_sp = ten_sp
        self.so_luong = so_luong
        self.don_gia = don_gia

    def tinh_thanh_tien(self) -> float:
        """Tính thành tiền"""
        return self.so_luong * self.don_gia

    def __str__(self):
        return f"{self.ten_sp} x{self.so_luong} = {self.tinh_thanh_tien():,.0f}đ"