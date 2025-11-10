from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Category


class CategoryDAO:
    """Data Access Object cho bảng category (MySQL)"""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_category(self, category: Category) -> bool:
        """Thêm danh mục mới (category_id tự tăng)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO category (category_name, category_des)
                VALUES (%s, %s)
            ''', (category.category_name, category.category_des))
            conn.commit()

            # Lấy ID vừa sinh ra
            category.category_id = cursor.lastrowid
            print(f"Đã thêm danh mục '{category.category_name}' (ID = {category.category_id})")
            return True
        except Error as e:
            print(f"Lỗi khi thêm danh mục: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def update_category(self, category: Category) -> bool:
        """Cập nhật danh mục"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE category
                SET category_name=%s, category_des=%s
                WHERE category_id=%s
            ''', (category.category_name, category.category_des, category.category_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật danh mục: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def delete_category(self, category_id: int) -> bool:
        """Xóa danh mục theo category_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM category WHERE category_id=%s', (category_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa danh mục: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def find_id_category(self, category_id: int) -> Optional[Category]:
        """Tìm danh mục theo category_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM category WHERE category_id=%s', (category_id,))
            row = cursor.fetchone()
            if row:
                return Category(row['category_id'], row['category_name'], row['category_des'])
            return None
        except Error as e:
            print(f"Lỗi khi tìm danh mục: {e}")
            return None
        finally:
            cursor.close()

    def list_category(self) -> List[Category]:
        """Lấy tất cả danh mục, sắp xếp theo tên"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM category ORDER BY category_name')
            rows = cursor.fetchall()
            return [Category(row['category_id'], row['category_name'], row['category_des']) for row in rows]
        except Error as e:
            print(f"Lỗi khi lấy danh sách danh mục: {e}")
            return []
        finally:
            cursor.close()
