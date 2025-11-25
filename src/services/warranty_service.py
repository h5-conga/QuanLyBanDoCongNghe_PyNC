from typing import Dict, Any
from src.dao.product_dao import ProductDAO
from src.dao.warranty_dao import WarrantyDAO


class WarrantyController:
    def __init__(self):
        self.warranty_dao = WarrantyDAO
        self.product_dao = ProductDAO

    def _build_response(self, thanh_cong: bool, thong_bao: str, du_lieu: Any = None) -> Dict[str, Any]:
        return {
            "thanh_cong": thanh_cong,
            "thong_bao": thong_bao,
            "du_lieu": du_lieu
        }

    def tra_cuu(self, ma_bao_hanh_str: str) -> Dict[str, Any]:
        if not ma_bao_hanh_str:
            return self._build_response(False, "Lỗi: Vui lòng nhập mã bảo hành.")

        try:
            warranty_id = int(ma_bao_hanh_str)
        except ValueError:
            return self._build_response(False, "Lỗi: Mã bảo hành phải là một con số.")
        except Exception as e:
            return self._build_response(False, f"Lỗi đầu vào không xác định: {e}")
        try:
            warranty = self.warranty_dao.find_by_id(warranty_id)
        except Exception as e:
            return self._build_response(False, f"Lỗi truy cập cơ sở dữ liệu: {e}")
        if not warranty:
            return self._build_response(False, f"Không tìm thấy phiếu bảo hành có mã: {warranty_id}")
        if warranty.check_time():
            ngay_het_han = warranty.end_date.strftime('%d/%m/%Y')
            thong_bao = f"Tìm thấy bảo hành. Sản phẩm CÒN HẠN đến ngày: {ngay_het_han}."
            return self._build_response(True, thong_bao, warranty)
        else:
            ngay_het_han = warranty.end_date.strftime('%d/%m/%Y')
            thong_bao = f"Tìm thấy bảo hành. Sản phẩm đã HẾT HẠN vào ngày: {ngay_het_han}."
            return self._build_response(True, thong_bao, warranty)

    def tra_cuu_theo_sdt(self, phone: str) -> Dict[str, Any]:
        try:
            warranties_list = self.warranty_dao.find_by_phone(phone)
            if not warranties_list:
                return self._build_response(False, f"Không tìm thấy bảo hành nào cho SĐT: {phone}")

            return self._build_response(True, f"Tìm thấy {len(warranties_list)} phiếu bảo hành.", warranties_list)

        except Exception as e:
            return self._build_response(False, f"Lỗi truy cập cơ sở dữ liệu: {e}")