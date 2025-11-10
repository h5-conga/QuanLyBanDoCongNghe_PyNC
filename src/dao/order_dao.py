from typing import Optional, List
from datetime import datetime
from mysql.connector import Error, IntegrityError
from QuanLyBanDoCongNghe_PyNC.src.config import DatabaseConnection
from QuanLyBanDoCongNghe_PyNC.src.models.entity import Order


# Giả sử bạn cũng có entity User và Customer để join, nhưng DAO này sẽ tập trung vào Order
# from QuanLyBanDoCongNghe_PyNC.src.models.entity import Customer, User


class OrderDAO:
    """
    Data Access Object (DAO) cho bảng 'order'.
    Quản lý thông tin tiêu đề của đơn hàng.
    LƯU Ý: DAO này KHÔNG quản lý bảng 'order_detail'.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def _row_to_order(self, row: dict) -> Order:
        """Hàm nội bộ: Chuyển đổi một dòng dữ liệu (dict) từ CSDL sang đối tượng Order."""
        # Khi tải từ CSDL, order_list sẽ mặc định là rỗng
        return Order(
            order_id=row['order_id'],
            customer_id=row['customer_id'],
            user_id=row['user_id'],
            date=row['date']
        )

    def add_order(self, order: Order) -> Optional[Order]:
        """
        Thêm một đơn hàng mới (chỉ thêm thông tin tiêu đề).
        'order_id' là AUTO_INCREMENT.
        Hàm sẽ trả về đối tượng Order đã được cập nhật 'order_id' mới.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Chỉ INSERT các cột có trong bảng 'order'
            cursor.execute('''
                INSERT INTO order (customer_id, user_id, date)
                VALUES (%s, %s, %s)
            ''', (order.customer_id, order.user_id, order.date))

            # Lấy ID tự động tăng
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

    def update_order_status(self, order_id: int, customer_id: int, user_id: int, date: datetime) -> bool:
        """Cập nhật thông tin tiêu đề đơn hàng."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE order
                SET customer_id=%s, user_id=%s, date=%s
                WHERE order_id=%s
            ''', (customer_id, user_id, date, order_id))

            conn.commit()
            affected = cursor.rowcount
            return affected > 0

        except Error as e:
            print(f"Lỗi khi cập nhật đơn hàng: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def delete_order(self, order_id: int) -> bool:
        """
        Xóa một đơn hàng.
        LƯU Ý: Thao tác này có thể thất bại nếu có 'order_detail'
        trỏ đến 'order_id' này (lỗi khóa ngoại).
        Bạn PHẢI xóa chi tiết đơn hàng trước.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM order WHERE order_id=%s', (order_id,))
            conn.commit()
            affected = cursor.rowcount
            return affected > 0

        except IntegrityError:
            print(f"Lỗi: Không thể xóa đơn hàng {order_id} vì vẫn còn chi tiết đơn hàng.")
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
        """
        Tìm đơn hàng theo ID.
        Trả về đối tượng Order với order_list rỗng [].
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM order WHERE order_id=%s', (order_id,))
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
        """
        Lấy danh sách tất cả đơn hàng, sắp xếp theo ngày mới nhất.
        Tất cả đối tượng Order trả về đều có order_list rỗng [].
        """
        orders = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            # Sắp xếp theo ngày giảm dần (mới nhất lên trước)
            cursor.execute('SELECT * FROM order ORDER BY date DESC')
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
        """Tìm tất cả đơn hàng của một khách hàng."""
        orders = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM order WHERE customer_id=%s ORDER BY date DESC', (customer_id,))
            rows = cursor.fetchall()

            for row in rows:
                orders.append(self._row_to_order(row))
            return orders
        except Error as e:
            print(f"Lỗi khi tìm đơn hàng theo khách hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()