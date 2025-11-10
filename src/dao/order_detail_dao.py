from datetime import datetime
from mysql.connector import Error
from typing import List
from src.models.entity import OrderDetail, Product
from src.config import DatabaseConnection

class OrderDetailDAO:
    """Data Access Object cho Chi tiết Đơn hàng"""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_order_detail(self, order_detail: OrderDetail, order_id: int) -> bool:
        """Thêm chi tiết đơn hàng"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO order_detail (order_id, product_id, quantity, start_date)
                VALUES (%s, %s, %s, %s)
            ''', (order_id, order_detail.product.product_id, order_detail.quantity, order_detail.start_date.isoformat()))

            conn.commit()
            return True
        except Error as e:
            print(f"Lỗi khi thêm chi tiết đơn hàng: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def get_order_details_by_order_id(self, order_id: int) -> List[OrderDetail]:
        """Lấy chi tiết của đơn hàng theo order_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)

            # Truy vấn để lấy chi tiết đơn hàng cùng với thông tin sản phẩm
            cursor.execute('''
                SELECT od.*, p.product_id, p.product_name, p.price
                FROM order_detail od
                JOIN product p ON od.product_id = p.product_id
                WHERE od.order_id = %s
            ''', (order_id,))

            order_details = []
            for row in cursor.fetchall():
                # Tạo đối tượng Product từ dữ liệu trả về
                product = Product(
                    product_id=row['product_id'],
                    product_name=row['product_name'],
                    price=row['price']
                )
                # Tạo OrderDetail với thông tin của sản phẩm và chi tiết đơn hàng
                order_detail = OrderDetail(
                    product=product,
                    quantity=row['quantity'],
                    start_date=datetime.fromisoformat(row['start_date'])
                )
                order_details.append(order_detail)

            return order_details
        except Error as e:
            print(f"Lỗi khi lấy chi tiết đơn hàng: {e}")
            return []
        finally:
            cursor.close()

    def delete_order_detail(self, order_id: int, product_id: int) -> bool:
        """Xóa chi tiết đơn hàng theo order_id và product_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM order_detail WHERE order_id = %s AND product_id = %s
            ''', (order_id, product_id))

            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa chi tiết đơn hàng: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def update_order_detail(self, order_id: int, product_id: int, order_detail: OrderDetail) -> bool:
        """Cập nhật chi tiết đơn hàng"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE order_detail
                SET quantity = %s, start_date = %s
                WHERE order_id = %s AND product_id = %s
            ''', (order_detail.quantity, order_detail.start_date.isoformat(), order_id, product_id))

            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật chi tiết đơn hàng: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
