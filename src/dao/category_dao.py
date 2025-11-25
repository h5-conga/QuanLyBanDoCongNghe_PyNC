from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Category


class CategoryDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_category(self, category_name: str, category_des: str) -> Optional[int]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO category (category_name, category_des)
                VALUES (%s, %s)
            ''', (category_name, category_des))
            conn.commit()

            new_id = cursor.lastrowid
            print(f"Đã thêm danh mục '{category_name}' (ID = {new_id})")
            return new_id
        except Error as e:
            print(f"Lỗi khi thêm danh mục: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()


    def update_category(self, category: Category) -> bool:
        conn = None
        cursor = None
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
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()


    def delete_category(self, category_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM category WHERE category_id=%s', (category_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa danh mục: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()


    def find_id_category(self, category_id: int) -> Optional[Category]:
        cursor = None
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
            if cursor:
                cursor.close()


    def list_category(self) -> List[Category]:
        cursor = None
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
            if cursor:
                cursor.close()