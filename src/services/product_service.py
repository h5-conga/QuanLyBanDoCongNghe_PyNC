from typing import List, Tuple, Optional, Dict, Union
from datetime import datetime
from src.dao.brand_dao import BrandDAO
from src.dao.category_dao import CategoryDAO
from src.dao.product_dao import ProductDAO
from src.models.entity import Product


class ProductService:
    def __init__(self):
        self.dao = ProductDAO()
        self.category_dao = CategoryDAO()
        self.brand_dao = BrandDAO()

    def add_product(self, product_data: Dict) -> Tuple[bool, Union[str, int]]:
        product_name = product_data.get('product_name')
        price = product_data.get('price')
        stock = product_data.get('stock_quantity')
        category_id = product_data.get('category_id')
        brand_id = product_data.get('brand_id')

        if not product_name:
            return False, "Tên sản phẩm không được để trống"

        if price is None or price <= 0:
            return False, "Giá bán phải lớn hơn 0"

        if stock is None or stock < 0:
            return False, "Số lượng tồn không được âm"

        if category_id is None or not self.category_dao.find_id_category(category_id):
            return False, "Danh mục không tồn tại"

        if brand_id is None or not self.brand_dao.find_id_brand(brand_id):
            return False, "Thương hiệu không tồn tại"

        product_data['description'] = product_data.get('description', "")
        product_data['entry_date'] = datetime.now()

        new_id = self.dao.add_product(product_data)
        if new_id:
            return True, new_id
        return False, "Thêm sản phẩm thất bại (Lỗi DAO)"

    def update_product(self, product: Product) -> Tuple[bool, str]:
        if not product.product_id:
            return False, "Mã sản phẩm không hợp lệ"
        if self.dao.update_product(product):
            return True, "Cập nhật sản phẩm thành công"
        return False, "Cập nhật sản phẩm thất bại"

    def get_all_products(self) -> List[Product]:
        return self.dao.list_products()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.dao.get_by_product_id(product_id)

    def find_by_product_name(self, tu_khoa: str) -> List[Product]:
        return self.dao.find_by_name(tu_khoa)

    def find_by_category(self, category_id: int) -> List[Product]:
        return self.dao.find_by_category_id(category_id)

    def find_by_brand(self, brand_id: int) -> List[Product]:
        return self.dao.find_by_brand_id(brand_id)

    def get_low_stock(self, threshold: int = 10) -> List[Product]:
        return self.dao.list_low_stock(threshold)

    def add_image_to_product(self, product_id: int, image_path: str, image_alt: str = "") -> bool:
        return self.dao.add_image(product_id, image_path, image_path, image_alt)

    def get_images_of_product(self, product_id: int) -> List[dict]:
        return self.dao.list_images_by_product(product_id)

    def delete_image(self, image_id: int) -> bool:
        return self.dao.delete_image(image_id)