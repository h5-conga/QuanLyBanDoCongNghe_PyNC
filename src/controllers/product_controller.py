from typing import List, Tuple, Optional, Dict
from src.models.entity import Product, Category, Brand
from src.services.product_service import ProductService
from src.controllers.category_controller import CategoryController
from src.controllers.brand_controller import BrandController


class ProductController:

    def __init__(self):
        self.product_service = ProductService()
        self.category_controller = CategoryController()
        self.brand_controller = BrandController()
        self.view = None
        self.categories: List[Category] = []
        self.brands: List[Brand] = []
        self.category_map: Dict[int, str] = {}
        self.brand_map: Dict[int, str] = {}
        self.rev_category_map: Dict[str, int] = {}
        self.rev_brand_map: Dict[str, int] = {}
        self.load_reference_data()

    def set_view(self, view):
        self.view = view

    def load_reference_data(self):
        self.categories = self.category_controller.get_all_categories()
        self.brands = self.brand_controller.get_all_brands()
        self.category_map = {c.category_id: c.category_name for c in self.categories}
        self.brand_map = {b.brand_id: b.brand_name for b in self.brands}
        self.rev_category_map = {c.category_name: c.category_id for c in self.categories}
        self.rev_brand_map = {b.brand_name: b.brand_id for b in self.brands}
    def get_category_names(self) -> List[str]:
        return list(self.rev_category_map.keys())

    def get_brand_names(self) -> List[str]:
        return list(self.rev_brand_map.keys())

    def get_full_product(self, product_id: int) -> Optional[Product]:
        return self.product_service.get_product_by_id(product_id)

    def _format_product_for_treeview(self, p: Product) -> tuple:
        brand_name = self.brand_map.get(p.brand_id, "N/A")
        category_name = self.category_map.get(p.category_id, "N/A")
        return (
            p.product_id, p.product_name, p.stock_quantity,
            f"{p.price:,.0f} VNĐ", f"{p.warranty_date} tháng",
            brand_name, category_name
        )

    def get_all_products_for_view(self) -> List[tuple]:
        products = self.product_service.get_all_products()
        return [self._format_product_for_treeview(p) for p in products]

    def search_products_for_view(self, keyword: str) -> List[tuple]:
        products = self.product_service.find_by_product_name(keyword)
        return [self._format_product_for_treeview(p) for p in products]

    def filter_by_category_for_view(self, category_name: str) -> List[tuple]:
        category_id = self.rev_category_map.get(category_name)
        if category_id:
            products = self.product_service.find_by_category(category_id)
            return [self._format_product_for_treeview(p) for p in products]
        return []

    def filter_by_brand_for_view(self, brand_name: str) -> List[tuple]:
        brand_id = self.rev_brand_map.get(brand_name)
        if brand_id:
            products = self.product_service.find_by_brand(brand_id)
            return [self._format_product_for_treeview(p) for p in products]
        return []

    def _remove_old_image_links(self, product_id: int):
        try:
            old_images = self.product_service.get_images_of_product(product_id)
            for img in old_images:
                img_id = img.get('image_id')
                if img_id:
                    self.product_service.delete_image(img_id)
            print(f"[Info] Đã gỡ bỏ liên kết ảnh cũ cho SP {product_id}")
        except Exception as e:
            print(f"[Warning] Lỗi khi gỡ ảnh cũ: {e}")

    def handle_add_product(self, data: dict) -> Tuple[bool, str]:
        try:
            category_id = self.rev_category_map.get(data['category_name'])
            brand_id = self.rev_brand_map.get(data['brand_name'])

            product_data = {
                "product_name": data['name'],
                "stock_quantity": data['quantity'],
                "price": data['price'],
                "cost_price": data['cost_price'],
                "warranty_date": data['warranty'],
                "description": data['description'],
                "category_id": category_id,
                "brand_id": brand_id,
            }
            success, msg_or_id = self.product_service.add_product(product_data)
            if not success:
                return False, str(msg_or_id)
            new_id = int(msg_or_id)
            image_path_absolute = data.get('image_path')

            if image_path_absolute:
                self.product_service.add_image_to_product(new_id, image_path_absolute, data['name'])

            if success:
                self.view.refresh_data()
            return True, f"Thêm sản phẩm thành công (ID: {new_id})"

        except Exception as e:
            return False, f"Lỗi hệ thống: {e}"

    def handle_update_product(self, data: dict) -> Tuple[bool, str]:
        try:
            product_id = data['product_id']

            category_id = self.rev_category_map.get(data['category_name'])
            brand_id = self.rev_brand_map.get(data['brand_name'])

            original_product = self.get_full_product(product_id)
            if not original_product:
                return False, "Sản phẩm không tồn tại"

            original_product.product_name = data['name']
            original_product.stock_quantity = data['quantity']
            original_product.price = data['price']
            original_product.cost_price = data['cost_price']
            original_product.warranty_date = data['warranty']
            original_product.description = data['description']
            original_product.category_id = category_id
            original_product.brand_id = brand_id

            success, msg = self.product_service.update_product(original_product)
            if not success:
                return False, msg

            new_image_path = data.get('image_path')

            if new_image_path:
                print(f"[Update] Cập nhật ảnh mới: {new_image_path}")

                self._remove_old_image_links(product_id)

                self.product_service.add_image_to_product(product_id, new_image_path, data['name'])

            self.view.refresh_data()
            return True, "Cập nhật sản phẩm thành công"

        except Exception as e:
            return False, f"Lỗi hệ thống: {e}"

    def handle_add_category(self, name: str, desc: str) -> Tuple[bool, str]:
        success, msg = self.category_controller.handle_add_category(name, desc)
        if success:
            self.load_reference_data()
            self.view.update_listbox()
        return success, msg

    def handle_add_brand(self, name: str, desc: str, country: str) -> Tuple[bool, str]:
        success, msg = self.brand_controller.handle_add_brand(name, desc, country)
        if success:
            self.load_reference_data()
            self.view.update_listbox()
        return success, msg