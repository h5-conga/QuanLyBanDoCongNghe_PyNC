from typing import List, Optional, Dict
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Product


class ProductDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def _create_product_from_row(self, row: dict) -> Optional[Product]:
        if not row:
            return None
        cat_name = row.pop('category_name', "")
        br_name = row.pop('brand_name', "")
        if 'image_id' not in row or row['image_id'] is None:
            row['image_id'] = None
        try:
            product = Product(**row)
            product.category_name = cat_name
            product.brand_name = br_name
            return product
        except TypeError as e:
            print(f"Lỗi dữ liệu khớp với Entity Product: {e}")
            return None

    def add_product(self, product_data: Dict) -> Optional[int]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO product 
                (product_name, price, stock_quantity, entry_date, warranty_date, cost_price, brand_id, category_id, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                product_data.get('product_name'), product_data.get('price'),
                product_data.get('stock_quantity'), product_data.get('entry_date'),
                product_data.get('warranty_date'), product_data.get('cost_price'),
                product_data.get('brand_id'), product_data.get('category_id'),
                product_data.get('description')
            ))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Lỗi khi thêm sản phẩm: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if cursor: cursor.close()

    def update_product(self, product: Product) -> bool:
        conn = None
        cursor = None
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
            return True
        except Error as e:
            print(f"Lỗi khi cập nhật sản phẩm: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def get_by_product_id(self, product_id: int) -> Optional[Product]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, 
                       c.category_name, 
                       b.brand_name,
                       img.min_image_id AS image_id
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN (
                    SELECT product_id, MIN(image_id) AS min_image_id
                    FROM product_image
                    GROUP BY product_id
                ) AS img ON p.product_id = img.product_id
                WHERE p.product_id = %s
            ''', (product_id,))
            row = cursor.fetchone()
            return self._create_product_from_row(row)
        except Error as e:
            print(f"Lỗi khi tìm sản phẩm: {e}")
            return None
        finally:
            if cursor: cursor.close()

    def list_products(self) -> List[Product]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, 
                       c.category_name, 
                       b.brand_name,
                       img.min_image_id AS image_id
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN (
                    SELECT product_id, MIN(image_id) AS min_image_id
                    FROM product_image
                    GROUP BY product_id
                ) AS img ON p.product_id = img.product_id
                ORDER BY p.product_id ASC
            ''')
            rows = cursor.fetchall()
            return [self._create_product_from_row(row) for row in rows if row]
        except Error as e:
            print(f"Lỗi khi lấy danh sách sản phẩm: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def list_low_stock(self, threshold: int = 10) -> List[Product]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, 
                       c.category_name, 
                       b.brand_name,
                       img.min_image_id AS image_id
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN (
                    SELECT product_id, MIN(image_id) AS min_image_id
                    FROM product_image
                    GROUP BY product_id
                ) AS img ON p.product_id = img.product_id
                WHERE p.stock_quantity <= %s
            ''', (threshold,))
            rows = cursor.fetchall()
            return [self._create_product_from_row(row) for row in rows if row]
        except Error as e:
            print(f"Lỗi khi lấy sản phẩm sắp hết hàng: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def find_by_name(self, keyword: str) -> List[Product]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, 
                       c.category_name, 
                       b.brand_name,
                       img.min_image_id AS image_id
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN (
                    SELECT product_id, MIN(image_id) AS min_image_id
                    FROM product_image
                    GROUP BY product_id
                ) AS img ON p.product_id = img.product_id
                WHERE p.product_name LIKE %s
            ''', (f'%{keyword}%',))
            rows = cursor.fetchall()
            return [self._create_product_from_row(row) for row in rows if row]
        except Error as e:
            print(f"Lỗi khi tìm sản phẩm theo tên: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def find_by_category_id(self, category_id: int) -> List[Product]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, 
                       c.category_name, 
                       b.brand_name,
                       img.min_image_id AS image_id
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN (
                    SELECT product_id, MIN(image_id) AS min_image_id
                    FROM product_image
                    GROUP BY product_id
                ) AS img ON p.product_id = img.product_id
                WHERE p.category_id = %s
                ORDER BY p.product_id ASC
            ''', (category_id,))
            rows = cursor.fetchall()
            return [self._create_product_from_row(row) for row in rows if row]
        except Error as e:
            print(f"Lỗi khi tìm sản phẩm theo danh mục: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def find_by_brand_id(self, brand_id: int) -> List[Product]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.*, 
                       c.category_name, 
                       b.brand_name,
                       img.min_image_id AS image_id
                FROM product p
                LEFT JOIN category c ON p.category_id = c.category_id
                LEFT JOIN brand b ON p.brand_id = b.brand_id
                LEFT JOIN (
                    SELECT product_id, MIN(image_id) AS min_image_id
                    FROM product_image
                    GROUP BY product_id
                ) AS img ON p.product_id = img.product_id
                WHERE p.brand_id = %s
                ORDER BY p.product_id ASC
            ''', (brand_id,))
            rows = cursor.fetchall()
            return [self._create_product_from_row(row) for row in rows if row]
        except Error as e:
            print(f"Lỗi khi tìm sản phẩm theo thương hiệu: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def add_image(self, product_id: int, image_url: str, image_path: str = "", image_alt: str = "") -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO product_image (product_id, image_url, image_path, image_alt)
                VALUES (%s, %s, %s, %s)
            ''', (product_id, image_url, image_path, image_alt))
            conn.commit()
            return True
        except Error as e:
            print(f"Lỗi khi thêm ảnh: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()

    def list_images_by_product(self, product_id: int) -> List[dict]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product_image WHERE product_id=%s', (product_id,))
            return cursor.fetchall()
        except Error as e:
            print(f"Lỗi khi lấy ảnh sản phẩm: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def delete_image(self, image_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM product_image WHERE image_id=%s', (image_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa ảnh: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()