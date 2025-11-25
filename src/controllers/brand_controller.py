from typing import List, Tuple, Optional
from src.services.brand_service import BrandService
from src.models.entity import Brand

class BrandController:
    def __init__(self):
        self.service = BrandService()

    def get_all_brands(self) -> List[Brand]:
        return self.service.get_list_brand()

    def get_brand_by_id(self, brand_id: int) -> Optional[Brand]:
        return self.service.find_brand_by_id(brand_id)

    def handle_add_brand(self, name: str, country: str, desc: str) -> Tuple[bool, str]:
        return self.service.add_brand(name, country, desc)

    def handle_update_brand(self, brand: Brand) -> Tuple[bool, str]:
        return self.service.update_brand(brand)

    def handle_delete_brand(self, brand_id: int) -> Tuple[bool, str]:
        return self.service.delete_brand(brand_id)