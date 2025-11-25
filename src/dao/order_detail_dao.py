from datetime import datetime
from mysql.connector import Error
from typing import List
from src.models.entity import OrderDetail, Product
from src.config import DatabaseConnection

class OrderDetailDAO:

    def __init__(self):
        self.db = DatabaseConnection()

    def add_order_detail(self, order_detail: OrderDetail, order_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            unit_price = order_detail.product.price
            total_amount = order_detail.quantity * unit_price

            cursor.execute('''
                INSERT INTO order_detail 
                (order_id, product_id, quantity, unit_price, total_amount, start_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                order_id,
                order_detail.product.product_id,
                order_detail.quantity,
                unit_price,
                total_amount,
                order_detail.start_date.isoformat()
            ))

            conn.commit()
            return True
        except Error as e:
            print(f"Lỗi khi thêm chi tiết đơn hàng: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def get_order_details_by_order_id(self, order_id: int) -> List[OrderDetail]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute('''
                SELECT od.*, p.product_name
                FROM order_detail od
                JOIN product p ON od.product_id = p.product_id
                WHERE od.order_id = %s
            ''', (order_id,))
            order_details = []
            for row in cursor.fetchall():
                product = Product(
                    product_id=row['product_id'],
                    image_id=None,
                    product_name=row['product_name'],
                    price=row['unit_price'],
                    stock_quantity=0,
                    entry_date=None,
                    warranty_date=0,
                    cost_price=0,
                    brand_id=None,
                    category_id=None
                )

                od = OrderDetail(
                    product=product,
                    quantity=row['quantity'],
                    start_date=datetime.fromisoformat(str(row['start_date']))
                )
                od.total_price = row['total_amount']
                order_details.append(od)

            return order_details
        except Error as e:
            print(f"Lỗi khi lấy chi tiết đơn hàng: {e}")
            return []
        finally:
            cursor.close()

    def delete_order_detail(self, order_id: int, product_id: int) -> bool:
        conn = None
        cursor = None
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
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            unit_price = order_detail.product.price
            total_amount = order_detail.quantity * unit_price
            cursor.execute('''
                UPDATE order_detail
                SET quantity = %s, unit_price = %s, total_amount = %s, start_date = %s
                WHERE order_id = %s AND product_id = %s
            ''', (
                order_detail.quantity,
                unit_price,
                total_amount,
                order_detail.start_date.isoformat(),
                order_id,
                product_id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật chi tiết đơn hàng: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()