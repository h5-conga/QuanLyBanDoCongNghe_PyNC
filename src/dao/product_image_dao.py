from typing import Optional, List
from mysql.connector import Error

from src.config import DatabaseConnection
from src.models.entity import ProductImage


class ProductImageDAO:
    """
    Data Access Object (DAO) cho bảng 'product_image'.
    Quản lý các hình ảnh liên quan đến sản phẩm.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def _row_to_image(self, row: dict) -> ProductImage:
        """Hàm nội bộ: Chuyển đổi một dòng dữ liệu (dict) từ CSDL sang đối tượng ProductImage."""
        return ProductImage(
            image_id=row['image_id'],
            product_id=row['product_id'],
            image_url=row['image_url'],
            image_path=row['image_path'],
            image_alt=row['image_alt']
        )

    def add_image(self, image: ProductImage) -> Optional[ProductImage]:
        """
        Thêm một ảnh mới vào CSDL.
        'image_id' là AUTO_INCREMENT nên không cần truyền vào.
        Trả về đối tượng ProductImage đã được cập nhật 'image_id' mới.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO product_image (product_id, image_url, image_path, image_alt)
                VALUES (%s, %s, %s, %s)
            ''', (image.product_id, image.image_url, image.image_path, image.image_alt))

            # Lấy ID tự động tăng
            new_id = cursor.lastrowid
            conn.commit()

            if new_id:
                image.image_id = new_id
                return image
            return None

        except Error as e:
            print(f"Lỗi khi thêm ảnh sản phẩm: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn:
                cursor.close()

    def delete_image(self, image_id: int) -> bool:
        """Xóa một ảnh khỏi CSDL dựa trên image_id."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM product_image WHERE image_id=%s', (image_id,))
            conn.commit()
            affected = cursor.rowcount
            return affected > 0

        except Error as e:
            print(f"Lỗi khi xóa ảnh sản phẩm: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def find_by_id(self, image_id: int) -> Optional[ProductImage]:
        """Tìm một ảnh cụ thể theo image_id."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product_image WHERE image_id=%s', (image_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_image(row)
            return None
        except Error as e:
            print(f"Lỗi khi tìm ảnh theo ID: {e}")
            return None
        finally:
            if conn:
                cursor.close()

    def find_by_product_id(self, product_id: int) -> List[ProductImage]:
        """
        Đây là hàm quan trọng: Lấy TẤT CẢ ảnh của một sản phẩm.
        Trả về một danh sách (List) các đối tượng ProductImage.
        """
        images = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM product_image WHERE product_id=%s', (product_id,))
            rows = cursor.fetchall()

            for row in rows:
                images.append(self._row_to_image(row))
            return images
        except Error as e:
            print(f"Lỗi khi lấy danh sách ảnh theo sản phẩm: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def update_image(self, image: ProductImage) -> bool:
        """Cập nhật thông tin của một ảnh (ví dụ: alt text, path)."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE product_image
                SET product_id=%s, image_url=%s, image_path=%s, image_alt=%s
                WHERE image_id=%s
            ''', (image.product_id, image.image_url, image.image_path,
                  image.image_alt, image.image_id))

            conn.commit()
            affected = cursor.rowcount
            return affected > 0

        except Error as e:
            print(f"Lỗi khi cập nhật ảnh sản phẩm: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def delete_by_product_id(self, product_id: int) -> bool:
        """
        (Hàm tiện ích) Xóa TẤT CẢ ảnh liên quan đến một sản phẩm.
        Hữu ích khi bạn xóa sản phẩm gốc.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM product_image WHERE product_id=%s', (product_id,))
            conn.commit()
            affected = cursor.rowcount
            return affected > 0

        except Error as e:
            print(f"Lỗi khi xóa ảnh theo ID sản phẩm: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()