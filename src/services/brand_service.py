from typing import List, Optional
from src.dao.brand_dao import BrandDAO
from src.models.entity import Brand


class BrandService:
    def __init__(self):
        self.dao = BrandDAO()

    def add_brand(self, brand_name: str, country: str, brand_des: str) -> tuple[bool, str]:
        if not brand_name:
            return False, "Tên thương hiệu không được để trống"

        new_id = self.dao.add_brand(brand_name, country, brand_des)
        if new_id:
            return True, f"Thêm thương hiệu thành công (ID: {new_id})"
        return False, "Thêm thương hiệu thất bại"

    def update_brand(self, brand: Brand) -> tuple[bool, str]:
        if not brand or not brand.brand_id:
            return False, "Đối tượng thương hiệu không hợp lệ"
        if not brand.brand_name:
            return False, "Tên thương hiệu không được để trống"

        if self.dao.update_brand(brand):
            return True, "Cập nhật thương hiệu thành công"
        return False, "Cập nhật thương hiệu thất bại"

    def delete_brand(self, brand_id: int) -> tuple[bool, str]:
        try:
            if self.dao.delete_brand(brand_id):
                return True, "Xóa thương hiệu thành công"
            return False, "Xóa thương hiệu thất bại (ID không tồn tại?)"
        except Exception as e:
            return False, f"Không thể xóa, có thể thương hiệu đang được sử dụng.\nLỗi: {e}"

    def get_list_brand(self) -> List[Brand]:
        return self.dao.list_brand()

    def find_brand_by_id(self, brand_id: int) -> Optional[Brand]:
        return self.dao.find_id_brand(brand_id)