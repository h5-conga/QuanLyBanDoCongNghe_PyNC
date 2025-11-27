from typing import List, Tuple, Optional, Dict
from src.dao.product_dao import ProductDAO
from src.dao.category_dao import CategoryDAO
from src.dao.brand_dao import BrandDAO
from src.services.product_service import ProductService
from src.models.entity import Product


class ProductController:
    def __init__(self):
        self.dao = ProductDAO()
        self.category_dao = CategoryDAO()
        self.brand_dao = BrandDAO()
        self.product_service = ProductService()
        self.view = None
        self.brand_map: Dict[int, str] = {}
        self.category_map: Dict[int, str] = {}
        self.refresh_maps()

    def set_view(self, view):
        self.view = view

    def refresh_maps(self):
        brands = self.brand_dao.list_brand()
        self.brand_map = {b.brand_id: b.brand_name for b in brands}
        cats = self.category_dao.list_category()
        self.category_map = {c.category_id: c.category_name for c in cats}

    def get_images_of_product(self, product_id: int) -> List[dict]:
        return self.product_service.get_images_of_product(product_id)

    def add_image_for_product(self, product_id: int, image_path: str) -> bool:
        return self.product_service.add_image_to_product(product_id, image_path)

    def delete_image_of_product(self, image_id: int) -> bool:
        return self.product_service.delete_image(image_id)

    def _convert_to_view_data(self, products: List[Product]) -> List[Tuple]:
        view_data = []
        for p in products:
            cat_name = getattr(p, 'category_name', self.category_map.get(p.category_id, "N/A"))
            brand_name = getattr(p, 'brand_name', self.brand_map.get(p.brand_id, "N/A"))
            formatted_price = "{:,.0f}".format(p.price) if p.price else "0"
            item = (
                p.product_id,
                p.product_name,
                p.stock_quantity,
                formatted_price,
                p.warranty_date,
                brand_name,
                cat_name
            )
            view_data.append(item)
        return view_data

    def get_all_products_for_view(self) -> List[Tuple]:
        self.refresh_maps()
        products = self.dao.list_products()
        return self._convert_to_view_data(products)

    def search_products_for_view(self, keyword: str) -> List[Tuple]:
        products = self.dao.find_by_name(keyword)
        return self._convert_to_view_data(products)

    def filter_by_category_for_view(self, category_name: str) -> List[Tuple]:
        cats = self.category_dao.list_category()
        found_cat = next((c for c in cats if c.category_name == category_name), None)
        if found_cat:
            products = self.dao.find_by_category_id(found_cat.category_id)
            return self._convert_to_view_data(products)
        return []

    def filter_by_brand_for_view(self, brand_name: str) -> List[Tuple]:
        brands = self.brand_dao.list_brand()
        found_brand = next((b for b in brands if b.brand_name == brand_name), None)
        if found_brand:
            products = self.dao.find_by_brand_id(found_brand.brand_id)
            return self._convert_to_view_data(products)
        return []

    def get_full_product(self, product_id: int) -> Optional[Product]:
        return self.dao.get_by_product_id(product_id)

    def get_category_names(self) -> List[str]:
        self.refresh_maps()
        return list(self.category_map.values())

    def get_brand_names(self) -> List[str]:
        self.refresh_maps()
        return list(self.brand_map.values())

    def handle_add_product(self, product_data: dict) -> Tuple[bool, str]:
        success, result = self.product_service.add_product(product_data)
        if success:
            return True, f"Thêm sản phẩm thành công (ID: {result})"
        return False, str(result)

    def handle_update_product(self, product: Product) -> Tuple[bool, str]:
        return self.product_service.update_product(product)

    def handle_add_category(self, name: str, desc: str) -> Tuple[bool, str]:
        if self.category_dao.add_category(name, desc):
            self.refresh_maps()
            return True, "Thêm danh mục thành công"
        return False, "Thêm danh mục thất bại"

    def handle_add_brand(self, name: str, desc: str, country: str) -> Tuple[bool, str]:
        if self.brand_dao.add_brand(name, country, desc):
            self.refresh_maps()
            return True, "Thêm thương hiệu thành công"
        return False, "Thêm thương hiệu thất bại"