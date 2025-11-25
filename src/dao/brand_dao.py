from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Brand


class BrandDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def add_brand(self, brand_name: str, country: str, brand_des: str) -> Optional[int]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO brand (brand_name, country, brand_des)
                VALUES (%s, %s, %s)
            ''', (brand_name, country, brand_des))
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Lỗi khi thêm thương hiệu: {e}")
            if conn:
                conn.rollback()
            return None
        finally:
            if cursor:
                cursor.close()

    def update_brand(self, brand: Brand) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE brand 
                SET brand_name = %s, country = %s, brand_des = %s
                WHERE brand_id = %s
            ''', (brand.brand_name, brand.country, brand.brand_des, brand.brand_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật thương hiệu: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_brand(self, brand_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM brand WHERE brand_id = %s', (brand_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa thương hiệu: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_id_brand(self, brand_id: int) -> Optional[Brand]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM brand WHERE brand_id = %s', (brand_id,))
            row = cursor.fetchone()
            if row:
                return Brand(
                    brand_id=row["brand_id"],
                    brand_name=row["brand_name"],
                    country=row["country"],
                    brand_des=row["brand_des"]
                )
            return None
        except Error as e:
            print(f"Lỗi khi tìm thương hiệu: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def list_brand(self) -> List[Brand]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM brand ORDER BY brand_name')
            rows = cursor.fetchall()
            return [
                Brand(
                    brand_id=row["brand_id"],
                    brand_name=row["brand_name"],
                    country=row["country"],
                    brand_des=row["brand_des"]
                )
                for row in rows
            ]
        except Error as e:
            print(f"Lỗi khi lấy danh sách thương hiệu: {e}")
            return []
        finally:
            if cursor:
                cursor.close()