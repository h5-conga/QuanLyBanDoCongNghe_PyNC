from typing import Optional, List
from datetime import datetime
from mysql.connector import Error, IntegrityError

from src.config import DatabaseConnection
from src.models.entity import Warranty


class WarrantyDAO:
    """
    Data Access Object (DAO) cho bảng 'warranty' (Bảo hành).
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def _row_to_warranty(self, row: dict) -> Warranty:
        """Hàm nội bộ: Chuyển đổi một dòng dữ liệu (dict) từ CSDL sang đối tượng Warranty."""
        # Lớp Warranty tự động tính end_date khi khởi tạo
        return Warranty(
            warranty_id=row['warranty_id'],
            product_id=row['product_id'],
            order_id=row['order_id'],
            customer_id=row['customer_id'],
            phone=row['phone'],
            start_date=row['start_date'],
            warranty_date=row['warranty_date']  # Đây là thời hạn (số tháng)
        )

    def add_warranty(self, warranty: Warranty) -> Optional[Warranty]:
        """
        Thêm một phiếu bảo hành mới.
        'warranty_id' là AUTO_INCREMENT.
        Hàm sẽ lưu 'end_date' đã được tính toán bởi lớp Warranty vào CSDL.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Chèn đầy đủ các trường, bao gồm cả end_date đã được tính
            cursor.execute('''
                INSERT INTO warranty (product_id, order_id, customer_id, phone, 
                                      start_date, warranty_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (warranty.product_id, warranty.order_id, warranty.customer_id, warranty.phone,
                  warranty.start_date, warranty.warranty_date, warranty.end_date))  # Lưu end_date

            # Lấy ID tự động tăng
            new_id = cursor.lastrowid
            conn.commit()

            if new_id:
                warranty.warranty_id = new_id
                return warranty
            return None

        except Error as e:
            print(f"Lỗi khi thêm bảo hành: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn:
                cursor.close()

    def find_by_id(self, warranty_id: int) -> Optional[Warranty]:
        """Tìm phiếu bảo hành theo ID."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM warranty WHERE warranty_id=%s', (warranty_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_warranty(row)
            return None
        except Error as e:
            print(f"Lỗi khi tìm bảo hành theo ID: {e}")
            return None
        finally:
            if conn:
                cursor.close()

    def find_by_phone(self, phone: str) -> List[Warranty]:
        """Tìm tất cả các phiếu bảo hành theo SĐT khách hàng."""
        warranties = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            # Sắp xếp cho phiếu sắp hết hạn lên trước
            cursor.execute('SELECT * FROM warranty WHERE phone=%s ORDER BY end_date ASC', (phone,))
            rows = cursor.fetchall()

            for row in rows:
                warranties.append(self._row_to_warranty(row))
            return warranties
        except Error as e:
            print(f"Lỗi khi tìm bảo hành theo SĐT: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def find_by_order_id(self, order_id: int) -> List[Warranty]:
        """Tìm tất cả bảo hành liên quan đến một đơn hàng."""
        warranties = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM warranty WHERE order_id=%s', (order_id,))
            rows = cursor.fetchall()

            for row in rows:
                warranties.append(self._row_to_warranty(row))
            return warranties
        except Error as e:
            print(f"Lỗi khi tìm bảo hành theo Đơn hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def find_by_customer_id(self, customer_id: int) -> List[Warranty]:
        """Tìm tất cả bảo hành của một khách hàng."""
        warranties = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM warranty WHERE customer_id=%s ORDER BY end_date DESC', (customer_id,))
            rows = cursor.fetchall()

            for row in rows:
                warranties.append(self._row_to_warranty(row))
            return warranties
        except Error as e:
            print(f"Lỗi khi tìm bảo hành theo Khách hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def delete_warranty(self, warranty_id: int) -> bool:
        """Xóa một phiếu bảo hành (ví dụ: khi hủy đơn)."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM warranty WHERE warranty_id=%s', (warranty_id,))
            conn.commit()
            affected = cursor.rowcount
            return affected > 0
        except Error as e:
            print(f"Lỗi khi xóa bảo hành: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def update_warranty(self, warranty: Warranty) -> bool:
        """Cập nhật thông tin bảo hành (ít dùng, nhưng nên có)."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE warranty
                SET product_id=%s, order_id=%s, customer_id=%s, phone=%s,
                    start_date=%s, warranty_date=%s, end_date=%s
                WHERE warranty_id=%s
            ''', (warranty.product_id, warranty.order_id, warranty.customer_id, warranty.phone,
                  warranty.start_date, warranty.warranty_date, warranty.end_date, warranty.warranty_id))

            conn.commit()
            affected = cursor.rowcount
            return affected > 0
        except Error as e:
            print(f"Lỗi khi cập nhật bảo hành: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()