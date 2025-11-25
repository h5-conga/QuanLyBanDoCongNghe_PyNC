from typing import Optional, List
from mysql.connector import Error, IntegrityError
from src.config import DatabaseConnection
from src.models.entity import Warranty


class WarrantyDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def _row_to_warranty(self, row: dict) -> Warranty:
        return Warranty(
            warranty_id=row['warranty_id'],
            product_id=row['product_id'],
            order_id=row['order_id'],
            customer_id=row['customer_id'],
            phone=row['phone'],
            start_date=row['start_date'],
            warranty_date=row['warranty_date']
        )

    def add_warranty(self, warranty: Warranty) -> Optional[Warranty]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO warranty (product_id, order_id, customer_id, phone, 
                                      start_date, warranty_date, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (warranty.product_id, warranty.order_id, warranty.customer_id, warranty.phone,
                  warranty.start_date, warranty.warranty_date, warranty.end_date))
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
        conn = None
        cursor = None
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
        warranties = []
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
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
        warranties = []
        conn = None
        cursor = None
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
        warranties = []
        conn = None
        cursor = None
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
        conn = None
        cursor = None
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
        conn = None
        cursor = None
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

    def get_all(self) -> List[Warranty]:
        warranties = []
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM warranty ORDER BY warranty_id DESC')
            rows = cursor.fetchall()

            for row in rows:
                warranties.append(self._row_to_warranty(row))
            return warranties
        except Error as e:
            print(f"Lỗi khi lấy danh sách bảo hành: {e}")
            return []
        finally:
            if conn:
                cursor.close()