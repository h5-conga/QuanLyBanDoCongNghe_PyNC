from datetime import datetime

class BaoHanh:
    """Lớp đại diện cho Bảo hành"""

    def __init__(self, ma_bao_hanh: str, ma_sp: str, ma_don_hang: str,
                 ngay_bat_dau: datetime, ngay_ket_thuc: datetime):
        self.ma_bao_hanh = ma_bao_hanh
        self.ma_sp = ma_sp
        self.ma_don_hang = ma_don_hang
        self.ngay_bat_dau = ngay_bat_dau
        self.ngay_ket_thuc = ngay_ket_thuc

    def kiem_tra_con_hieu_luc(self) -> bool:
        """Kiểm tra bảo hành còn hiệu lực"""
        return datetime.now() <= self.ngay_ket_thuc