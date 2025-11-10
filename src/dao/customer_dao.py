from typing import Optional, List
from mysql.connector import IntegrityError, Error
from QuanLyBanDoCongNghe_PyNC.src.config import DatabaseConnection
from QuanLyBanDoCongNghe_PyNC.src.models.entity import Customer


class CustomerDAO:
    """
    Data Access Object (DAO) cho bảng 'customer'.
    Thực hiện tất cả các thao tác CRUD (Thêm, Đọc, Sửa, Xóa)
    với CSDL MySQL.
    """

    def __init__(self):
        self.db = DatabaseConnection()

    def _row_to_customer(self, row: dict) -> Customer:
        """Hàm nội bộ: Chuyển đổi một dòng dữ liệu (dict) từ CSDL sang đối tượng Customer."""
        return Customer(
            customer_id=row['customer_id'],
            customer_name=row['customer_name'],
            phone=row['phone'],
            address=row['address'],
            email=row['email']
        )

    def add_customer(self, customer: Customer) -> Optional[Customer]:
        """
        Thêm một khách hàng mới vào CSDL.

        Vì 'customer_id' là AUTO_INCREMENT, chúng ta không cần truyền nó vào.
        Hàm sẽ trả về chính đối tượng Customer đó nhưng đã được CSDL
        cập nhật 'customer_id' mới.
        """
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            # Câu lệnh INSERT không chứa 'customer_id'
            cursor.execute('''
                INSERT INTO customer (customer_name, phone, address, email)
                VALUES (%s, %s, %s, %s)
            ''', (customer.customer_name, customer.phone, customer.address, customer.email))

            # Lấy ID tự động tăng vừa được tạo
            new_id = cursor.lastrowid
            conn.commit()

            if new_id:
                # Cập nhật ID cho đối tượng Python và trả về
                customer.customer_id = new_id
                return customer
            return None

        except IntegrityError:
            # Xử lý lỗi nếu SĐT hoặc Email bị trùng (nếu bạn có thêm UNIQUE)
            if conn: conn.rollback()
            return None
        except Error as e:
            print(f"Lỗi khi thêm khách hàng: {e}")
            if conn: conn.rollback()
            return None
        finally:
            if conn:
                cursor.close()

    def update_customer(self, customer: Customer) -> bool:
        """Cập nhật thông tin khách hàng dựa trên customer_id."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE customer
                SET customer_name=%s, phone=%s, address=%s, email=%s
                WHERE customer_id=%s
            ''', (customer.customer_name, customer.phone,
                  customer.address, customer.email, customer.customer_id))

            conn.commit()
            affected = cursor.rowcount
            return affected > 0  # Trả về True nếu có dòng bị ảnh hưởng (cập nhật thành công)

        except Error as e:
            print(f"Lỗi khi cập nhật khách hàng: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def delete_customer(self, customer_id: int) -> bool:
        """Xóa khách hàng theo ID."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            # Cần xử lý ràng buộc khóa ngoại (ví dụ: không thể xóa KH nếu họ có đơn hàng)
            # Trong ví dụ này, ta giả định có thể xóa hoặc CSDL tự xử lý (ON DELETE SET NULL/CASCADE)
            cursor.execute('DELETE FROM customer WHERE customer_id=%s', (customer_id,))
            conn.commit()
            affected = cursor.rowcount
            return affected > 0

        except IntegrityError as e:
            print(f"Lỗi ràng buộc khóa ngoại khi xóa KH: {e}")
            if conn: conn.rollback()
            return False
        except Error as e:
            print(f"Lỗi khi xóa khách hàng: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if conn:
                cursor.close()

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        """Tìm khách hàng theo ID."""
        conn = None
        try:
            conn = self.db.get_connection()
            # dictionary=True: Trả về kết quả dưới dạng dict (giống tên cột)
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customer WHERE customer_id=%s', (customer_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_customer(row)
            return None
        except Error as e:
            print(f"Lỗi khi tìm khách hàng theo ID: {e}")
            return None
        finally:
            if conn:
                cursor.close()

    def find_by_phone(self, phone: str) -> Optional[Customer]:
        """Tìm khách hàng theo số điện thoại (chỉ trả về kết quả đầu tiên nếu trùng)."""
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customer WHERE phone=%s', (phone,))
            row = cursor.fetchone()

            if row:
                return self._row_to_customer(row)
            return None
        except Error as e:
            print(f"Lỗi khi tìm khách hàng theo SĐT: {e}")
            return None
        finally:
            if conn:
                cursor.close()

    def list_all_customers(self) -> List[Customer]:
        """Lấy danh sách tất cả khách hàng, sắp xếp theo tên."""
        customers = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM customer ORDER BY customer_name')
            rows = cursor.fetchall()

            for row in rows:
                customers.append(self._row_to_customer(row))
            return customers
        except Error as e:
            print(f"Lỗi khi lấy danh sách khách hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()

    def search_by_name_or_phone(self, keyword: str) -> List[Customer]:
        """Tìm kiếm khách hàng theo Tên hoặc SĐT (dùng LIKE)."""
        customers = []
        conn = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            query_keyword = f"%{keyword}%"  # Thêm ký tự đại diện %

            cursor.execute('''
                SELECT * FROM customer 
                WHERE customer_name LIKE %s OR phone LIKE %s
                ORDER BY customer_name
            ''', (query_keyword, query_keyword))

            rows = cursor.fetchall()
            for row in rows:
                customers.append(self._row_to_customer(row))
            return customers
        except Error as e:
            print(f"Lỗi khi tìm kiếm khách hàng: {e}")
            return []
        finally:
            if conn:
                cursor.close()