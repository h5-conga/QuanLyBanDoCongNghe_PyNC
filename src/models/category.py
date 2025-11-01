class DanhMuc:
    """Lớp đại diện cho Danh mục sản phẩm"""

    def __init__(self, ma_danh_muc: str, ten_danh_muc: str, mo_ta: str = ""):
        self.ma_danh_muc = ma_danh_muc
        self.ten_danh_muc = ten_danh_muc
        self.mo_ta = mo_ta

    def __str__(self):
        return f"DM[{self.ma_danh_muc}] {self.ten_danh_muc}"