from typing import List, Optional
from src.dao.category_dao import CategoryDAO
from src.models.entity import Category


class CategoryService:
    def __init__(self):
        self.dao = CategoryDAO()

    def add_category(self, category_name: str, category_des: str) -> tuple[bool, str]:
        if not category_name:
            return False, "Tên danh mục không được để trống"

        new_id = self.dao.add_category(category_name, category_des)
        if new_id:
            return True, f"Thêm danh mục thành công (ID: {new_id})"
        return False, "Thêm danh mục thất bại"

    def update_category(self, category: Category) -> tuple[bool, str]:
        if not category or not category.category_id:
            return False, "Đối tượng danh mục không hợp lệ"
        if not category.category_name:
            return False, "Tên danh mục không được để trống"

        if self.dao.update_category(category):
            return True, "Cập nhật danh mục thành công"
        return False, "Cập nhật danh mục thất bại"

    def delete_category(self, category_id: int) -> tuple[bool, str]:
        try:
            if self.dao.delete_category(category_id):
                return True, "Xóa danh mục thành công"
            return False, "Xóa danh mục thất bại (ID không tồn tại?)"
        except Exception as e:
            return False, f"Không thể xóa, có thể danh mục đang được sử dụng.\nLỗi: {e}"

    def get_list_category(self) -> List[Category]:
        return self.dao.list_category()

    def find_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.dao.find_id_category(category_id)