from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Brand


class BrandDAO:
    """Data Access Object cho bảng Thương hiệu (brand)"""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_brand(self, brand: Brand) -> bool:
        """Thêm thương hiệu mới (brand_id tự tăng)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO brand (brand_name, country, brand_des)
                VALUES (%s, %s, %s)
            ''', (brand.brand_name, brand.country, brand.brand_des))
            conn.commit()
            # Lấy id vừa được sinh ra
            brand.brand_id = cursor.lastrowid
            print(f"Đã thêm thương hiệu '{brand.brand_name}' (ID = {brand.brand_id})")

            return True
        except Error as e:
            print(f"Lỗi khi thêm thương hiệu: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def update_brand(self, brand: Brand) -> bool:
        """Cập nhật thông tin thương hiệu"""
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
            conn.rollback()
            return False
        finally:
            cursor.close()

    def delete_brand(self, brand_id: int) -> bool:
        """Xóa thương hiệu theo ID"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM brand WHERE brand_id = %s', (brand_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa thương hiệu: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def find_id_brand(self, brand_id: int) -> Optional[Brand]:
        """Tìm thương hiệu theo ID"""
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
            cursor.close()

    def list_brand(self) -> List[Brand]:
        """Lấy danh sách tất cả thương hiệu"""
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
            cursor.close()
