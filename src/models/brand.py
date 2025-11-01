class ThuongHieu:
    """Lớp đại diện cho Thương hiệu"""

    def __init__(self, ma_thuong_hieu: str, ten_thuong_hieu: str,
                 quoc_gia: str = "", mo_ta: str = ""):
        self.ma_thuong_hieu = ma_thuong_hieu
        self.ten_thuong_hieu = ten_thuong_hieu
        self.quoc_gia = quoc_gia
        self.mo_ta = mo_ta

    def __str__(self):
        return f"TH[{self.ma_thuong_hieu}] {self.ten_thuong_hieu} ({self.quoc_gia})"