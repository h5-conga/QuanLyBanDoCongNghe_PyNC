from typing import Optional, List
from mysql.connector import Error, IntegrityError
from src.config import DatabaseConnection
from src.models.entity import Order


class OrderDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def _row_to_order(self, row: dict) -> Order:
        date_value = row['date']
        if date_value:
            date_value = date_value.strftime("%d-%m-%Y")
        return Order(
            order_id=row['order_id'],
            customer_id=row['customer_id'],
            user_id=row['user_id'],
            date=date_value
        )

    def add_order(self, order: Order) -> Optional[Order]:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO `order` (customer_id, user_id)
                VALUES (%s, %s)
            ''', (order.customer_id, order.user_id))
            new_id = cursor.lastrowid
            conn.commit()
            if new_id:
                order.order_id = new_id
                return order
            return None
        except Error as e:
            print(f"Lỗi khi thêm đơn hàng: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn:
                cursor.close()

    def update_order(self, order_id: int, customer_id: int, user_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE `order`
                SET customer_id=%s, user_id=%s
                WHERE order_id=%s
            ''', (customer_id, user_id, order_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật đơn hàng: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def delete_order(self, order_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM `order` WHERE order_id=%s', (order_id,))
            conn.commit()
            return cursor.rowcount > 0
        except IntegrityError:
            print(f"Lỗi: không thể xóa đơn hàng {order_id} vì còn order_detail.")
            if conn: conn.rollback()
            return False
        except Error as e:
            print(f"Lỗi khi xóa đơn hàng: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def find_by_id(self, order_id: int) -> Optional[Order]:
        conn = None
        cursor=None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM `order` WHERE order_id=%s', (order_id,))
            row = cursor.fetchone()
            if row:
                return self._row_to_order(row)
            return None
        except Error as e:
            print(f"Lỗi khi tìm đơn hàng theo ID: {e}")
            return None
        finally:
            if conn:
                cursor.close()

    def list_all_orders(self) -> List[Order]:
        orders = []
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM `order` ORDER BY order_id ASC')
            rows = cursor.fetchall()
            for row in rows:
                orders.append(self._row_to_order(row))
            return orders
        except Error as e:
            print(f"Lỗi khi lấy danh sách đơn hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def find_by_customer_id(self, customer_id: int) -> List[Order]:
        orders = []
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM `order` WHERE customer_id=%s ORDER BY order_id ASC',
                           (customer_id,))
            for row in cursor.fetchall():
                orders.append(self._row_to_order(row))
            return orders
        except Error as e:
            print(f"Lỗi khi tìm đơn hàng theo khách hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def find_by_customer_name(self, customer_name: str) -> List[Order]:
        orders = []
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT o.*
                FROM `order` o
                JOIN customer c ON o.customer_id = c.customer_id
                WHERE c.customer_name LIKE %s
                ORDER BY o.order_id ASC
            """, (f"%{customer_name}%",))
            for row in cursor.fetchall():
                orders.append(self._row_to_order(row))
            return orders
        except Error as e:
            print(f"Lỗi khi tìm đơn hàng theo tên khách: {e}")
            return []
        finally:
            if conn:
                cursor.close()