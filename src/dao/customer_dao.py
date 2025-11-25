from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import Customer


class CustomerDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def get_all_customers(self) -> List[Customer]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customer ORDER BY customer_id ASC')
            rows = cursor.fetchall()
            customers = []
            for row in rows:
                customers.append(Customer(
                    customer_id=row['customer_id'],
                    customer_name=row['customer_name'],
                    phone=row['phone'],
                    address=row['address'],
                    email=row['email']
                ))
            return customers
        except Error as e:
            print(f"Lỗi khi lấy danh sách khách hàng: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def add_customer(self, customer: Customer) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customer (customer_name, phone, address, email)
                VALUES (%s, %s, %s, %s)
            ''', (customer.customer_name, customer.phone, customer.address, customer.email))
            conn.commit()
            if cursor.lastrowid:
                customer.customer_id = cursor.lastrowid
            return True
        except Error as e:
            print(f"Lỗi khi thêm khách hàng: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def update_customer(self, customer: Customer) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE customer
                SET customer_name=%s, phone=%s, address=%s, email=%s
                WHERE customer_id=%s
            ''', (customer.customer_name, customer.phone, customer.address, customer.email, customer.customer_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def delete_customer(self, customer_id: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM customer WHERE customer_id=%s', (customer_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def search_customers(self, keyword: str) -> List[Customer]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            search_query = f"%{keyword}%"
            cursor.execute('''
                SELECT * FROM customer 
                WHERE customer_name LIKE %s OR phone LIKE %s
            ''', (search_query, search_query))
            rows = cursor.fetchall()
            return [
                Customer(
                    customer_id=row['customer_id'],
                    customer_name=row['customer_name'],
                    phone=row['phone'],
                    address=row['address'],
                    email=row['email']
                ) for row in rows
            ]
        except Error as e:
            print(f"Lỗi khi tìm kiếm khách hàng: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customer WHERE customer_id=%s', (customer_id,))
            row = cursor.fetchone()
            if row:
                return Customer(
                    customer_id=row['customer_id'],
                    customer_name=row['customer_name'],
                    phone=row['phone'],
                    address=row['address'],
                    email=row['email']
                )
            return None
        except Error as e:
            print(f"Lỗi khi tìm khách hàng theo ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()