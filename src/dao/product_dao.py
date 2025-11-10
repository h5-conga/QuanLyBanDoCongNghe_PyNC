from typing import List, Optional
from datetime import datetime
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Product  # Chú ý sửa đường dẫn nếu khác

class ProductDAO:
    """Data Access Object cho bảng Product"""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_product(self, product: Product) -> bool:
        """Thêm sản phẩm mới"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO product 
                (product_name, price, stock_quantity, entry_date, warranty_date, cost_price, brand_id, category_id, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (product.product_name, product.price, product.stock_quantity,
                  product.entry_date, product.warranty_date, product.cost_price,
                  product.brand_id, product.category_id, product.description))
            conn.commit()
            product.product_id = cursor.lastrowid
            return True
        except Error as e:
            print(f"Lỗi khi thêm sản phẩm: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def update_product(self, product: Product) -> bool:
        """Cập nhật sản phẩm"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE product
                SET product_name=%s, price=%s, stock_quantity=%s, entry_date=%s,
                    warranty_date=%s, cost_price=%s, brand_id=%s, category_id=%s, description=%s
                WHERE product_id=%s
            ''', (product.product_name, product.price, product.stock_quantity, product.entry_date,
                  product.warranty_date, product.cost_price, product.brand_id, product.category_id,
                  product.description, product.product_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật sản phẩm: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def get_by_product_id(self, product_id: int) -> Optional[Product]:
        """Tìm sản phẩm theo ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product WHERE product_id=%s', (product_id,))
            row = cursor.fetchone()
            if row:
                return Product(**row)
            return None
        except Error as e:
            print(f"Lỗi khi tìm sản phẩm: {e}")
            return None
        finally:
            cursor.close()

    def list_products(self) -> List[Product]:
        """Lấy tất cả sản phẩm"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product ORDER BY product_name')
            rows = cursor.fetchall()
            return [Product(**row) for row in rows]
        except Error as e:
            print(f"Lỗi khi lấy danh sách sản phẩm: {e}")
            return []
        finally:
            cursor.close()

    def list_low_stock(self, threshold: int = 10) -> List[Product]:
        """Lấy sản phẩm sắp hết hàng"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product WHERE stock_quantity <= %s', (threshold,))
            rows = cursor.fetchall()
            return [Product(**row) for row in rows]
        except Error as e:
            print(f"Lỗi khi lấy sản phẩm sắp hết hàng: {e}")
            return []
        finally:
            cursor.close()

    def search_by_name(self, keyword: str) -> List[Product]:
        """Tìm sản phẩm theo tên"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product WHERE product_name LIKE %s', (f'%{keyword}%',))
            rows = cursor.fetchall()
            return [Product(**row) for row in rows]
        except Error as e:
            print(f"Lỗi khi tìm sản phẩm theo tên: {e}")
            return []
        finally:
            cursor.close()
