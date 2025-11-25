from typing import List, Dict
from mysql.connector import Error

from src.config import DatabaseConnection


class StatisticsService:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_revenue_by_time(self, time_type: str) -> List[Dict]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)

            if time_type == 'month':
                sql = '''
                    SELECT 
                        DATE_FORMAT(o.date, '%m/%Y') as time_label,
                        SUM(od.total_amount) as revenue,
                        COUNT(DISTINCT o.order_id) as order_count
                    FROM `order` o
                    JOIN order_detail od ON o.order_id = od.order_id
                    GROUP BY DATE_FORMAT(o.date, '%m/%Y')
                    ORDER BY MAX(o.date) ASC
                '''
            elif time_type == 'quarter':
                sql = '''
                    SELECT 
                        CONCAT('Q', QUARTER(o.date), '/', YEAR(o.date)) as time_label,
                        SUM(od.total_amount) as revenue,
                        COUNT(DISTINCT o.order_id) as order_count
                    FROM `order` o
                    JOIN order_detail od ON o.order_id = od.order_id
                    GROUP BY CONCAT('Q', QUARTER(o.date), '/', YEAR(o.date))
                    ORDER BY MAX(o.date) ASC
                '''
            elif time_type == 'year':
                sql = '''
                    SELECT 
                        DATE_FORMAT(o.date, '%Y') as time_label,
                        SUM(od.total_amount) as revenue,
                        COUNT(DISTINCT o.order_id) as order_count
                    FROM `order` o
                    JOIN order_detail od ON o.order_id = od.order_id
                    GROUP BY DATE_FORMAT(o.date, '%Y')
                    ORDER BY time_label ASC
                '''
            else:
                return []

            cursor.execute(sql)
            return cursor.fetchall()

        except Error as e:
            print(f"Lỗi thống kê doanh thu: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def get_top_products(self, limit=5) -> List[Dict]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = '''
                SELECT 
                    p.product_name as name,
                    SUM(od.quantity) as total_qty,
                    SUM(od.total_amount) as revenue
                FROM order_detail od
                JOIN product p ON od.product_id = p.product_id
                GROUP BY p.product_id, p.product_name 
                ORDER BY revenue DESC
                LIMIT %s
            '''
            cursor.execute(sql, (limit,))
            return cursor.fetchall()
        except Error as e:
            print(f"Lỗi thống kê top sản phẩm: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def get_revenue_custom_range(self, start_date, end_date) -> Dict:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = '''
                SELECT 
                    COALESCE(SUM(od.total_amount), 0) as total_revenue,
                    COUNT(DISTINCT o.order_id) as total_orders
                FROM `order` o
                JOIN order_detail od ON o.order_id = od.order_id
                WHERE o.date BETWEEN %s AND %s
            '''
            cursor.execute(sql, (start_date, end_date))
            result = cursor.fetchone()
            return result if result else {'total_revenue': 0, 'total_orders': 0}
        except Error as e:
            print(f"Lỗi thống kê tùy chỉnh: {e}")
            return {'total_revenue': 0, 'total_orders': 0}
        finally:
            if cursor: cursor.close()

    def get_revenue_daily_in_range(self, start_date, end_date) -> List[Dict]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = '''
                SELECT 
                    DATE_FORMAT(o.date, '%d/%m/%Y') as date_label,
                    SUM(od.total_amount) as revenue,
                    COUNT(DISTINCT o.order_id) as order_count
                FROM `order` o
                JOIN order_detail od ON o.order_id = od.order_id
                WHERE o.date BETWEEN %s AND %s
                GROUP BY DATE_FORMAT(o.date, '%d/%m/%Y')
                ORDER BY MAX(o.date) ASC
            '''
            cursor.execute(sql, (start_date, end_date))
            return cursor.fetchall()
        except Error as e:
            print(f"Lỗi thống kê chi tiết tùy chỉnh: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def get_top_products_by_quantity(self, limit=5) -> List[Dict]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            sql = '''
                SELECT 
                    p.product_name as name,
                    SUM(od.quantity) as total_qty,
                    SUM(od.total_amount) as revenue
                FROM order_detail od
                JOIN product p ON od.product_id = p.product_id
                GROUP BY p.product_id, p.product_name 
                ORDER BY total_qty DESC
                LIMIT %s
            '''
            cursor.execute(sql, (limit,))
            return cursor.fetchall()
        except Error as e:
            print(f"Lỗi thống kê top sản phẩm theo số lượng: {e}")
            return []
        finally:
            if cursor: cursor.close()