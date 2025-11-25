from typing import List, Tuple, Optional
from src.services.category_service import CategoryService
from src.models.entity import Category

class CategoryController:
    def __init__(self):
        self.service = CategoryService()

    def get_all_categories(self) -> List[Category]:
        return self.service.get_list_category()

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.service.find_category_by_id(category_id)

    def handle_add_category(self, name: str, desc: str) -> Tuple[bool, str]:
        return self.service.add_category(name, desc)

    def handle_update_category(self, category: Category) -> Tuple[bool, str]:
        return self.service.update_category(category)

    def handle_delete_category(self, category_id: int) -> Tuple[bool, str]:
        return self.service.delete_category(category_id)