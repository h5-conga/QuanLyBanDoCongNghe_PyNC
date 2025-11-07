from typing import Optional, List
from mysql.connector import IntegrityError
from src.config import DatabaseConnection
from src.models.entity import Category


class DanhMucDAO:
    """Data Access Object cho bảng category (MySQL)"""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_category(self, category: Category) -> bool:
        """Thêm danh mục mới"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO category (category_id, category_name, category_des)
                VALUES (%s, %s, %s)
            ''', (category.category_id, category.category_name, category.category_des))
            conn.commit()
            cursor.close()
            return True
        except IntegrityError:
            return False

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
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        except:
            return False

    def delete_category(self, category_id: str) -> bool:
        """Xóa danh mục theo category_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM category WHERE category_id=%s', (category_id,))
            conn.commit()
            affected = cursor.rowcount
            cursor.close()
            return affected > 0
        except:
            return False

    def find_id_category(self, category_id: str) -> Optional[Category]:
        """Tìm danh mục theo category_id"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM category WHERE category_id=%s', (category_id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            return Category(row['category_id'], row['category_name'], row['category_des'])
        return None

    def list_category(self) -> List[Category]:
        """Lấy tất cả danh mục, sắp xếp theo tên"""
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM category ORDER BY category_name')
        rows = cursor.fetchall()
        cursor.close()
        return [Category(row['category_id'], row['category_name'], row['category_des']) for row in rows]
