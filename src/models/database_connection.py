import mysql.connector
from mysql.connector import Error
from datetime import datetime

class DatabaseConnection:
    """Singleton pattern cho kết nối MySQL"""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _create_database_if_not_exists(self):
        """Tạo database nếu chưa tồn tại"""
        try:
            temp_conn = mysql.connector.connect(
                host='localhost',
                port=3306,          # Port phải là số
                user='root',        # Thay user MySQL của bạn
                password='123123'   # Thay password MySQL của bạn
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute("CREATE DATABASE IF NOT EXISTS sales_management")
            temp_cursor.close()
            temp_conn.close()
        except Error as e:
            print(f"Lỗi khi tạo database: {e}")
            raise

    def get_connection(self):
        """Lấy kết nối đến MySQL"""
        if self._connection is None:
            try:
                # Bước 1: Tạo database nếu chưa có
                self._create_database_if_not_exists()

                # Bước 2: Kết nối tới database vừa tạo
                self._connection = mysql.connector.connect(
                    host='localhost',
                    port=3306,
                    user='root',
                    password='123123',
                    database='sales_management',
                    autocommit=False
                )
                self._init_database()
            except Error as e:
                print(f"Lỗi kết nối MySQL: {e}")
                raise
        return self._connection

    def _init_database(self):
        """Khởi tạo các bảng nếu chưa tồn tại"""
        cursor = self._connection.cursor()

        # Bảng danh mục
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                category_id VARCHAR(20) PRIMARY KEY,
                category_name NVARCHAR(255) NOT NULL,
                category_des TEXT
            )
        ''')

        # Bảng thương hiệu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brand (
                brand_id VARCHAR(20) PRIMARY KEY,
                brand_name NVARCHAR(255) NOT NULL,
                country VARCHAR(100),
                brand_des TEXT
            )
        ''')

        # Bảng user
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                user_id VARCHAR(20) PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fullname NVARCHAR(255) NOT NULL,
                role VARCHAR(50),
                status_user VARCHAR(50) DEFAULT 'active',
            )
        ''')

        # Bảng product_image
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_images (
                image_id VARCHAR(255) PRIMARY KEY,
                product_id VARCHAR(255) NOT NULL,
                image_url VARCHAR(255) NOT NULL,
                image_path VARCHAR(255) NOT NULL,
                image_alt VARCHAR(255),
                FOREIGN KEY (product_id) REFERENCES product(product_id)
            )
        """)

        # Bảng sản phẩm
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product (
                product_id VARCHAR(20) PRIMARY KEY,
                image_id VARCHAR(20) NOT NULL
                product_name NVARCHAR(255) NOT NULL,
                category_id VARCHAR(20),
                brand_id VARCHAR(20),
                price DECIMAL(15,2),
                stock_quantity INT,
                entry_date DATETIME,
                warranty_date INT,
                description TEXT,
                cost_price DECIMAL(15,2),
                FOREIGN KEY (category_id) REFERENCES category(category_id),
                FOREIGN KEY (brand_id) REFERENCES brand(brand_id)
            )
        ''')

        # Bảng khách hàng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer (
                customer_id VARCHAR(20) PRIMARY KEY,
                customer_name NVARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                email VARCHAR(255)
            )
        ''')

        # Bảng đơn hàng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order (
                order_id VARCHAR(20) PRIMARY KEY,
                customer_id VARCHAR(20),
                user_id VARCHAR(20),
                ngay_tao DATETIME,
                trang_thai VARCHAR(50),
                tong_tien DECIMAL(15,2),
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
            )
        ''')

        # Bảng chi tiết đơn hàng
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chi_tiet_don_hang (
                id INT AUTO_INCREMENT PRIMARY KEY,
                ma_don_hang VARCHAR(20),
                ma_sp VARCHAR(20),
                ten_sp VARCHAR(255),
                so_luong INT,
                don_gia DECIMAL(15,2),
                thanh_tien DECIMAL(15,2),
                FOREIGN KEY (ma_don_hang) REFERENCES don_hang(ma_don_hang),
                FOREIGN KEY (ma_sp) REFERENCES san_pham(ma_sp)
            )
        ''')

        # Bảng bảo hành
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bao_hanh (
                ma_bao_hanh VARCHAR(20) PRIMARY KEY,
                ma_sp VARCHAR(20),
                ma_don_hang VARCHAR(20),
                ngay_bat_dau DATETIME,
                ngay_ket_thuc DATETIME,
                FOREIGN KEY (ma_sp) REFERENCES san_pham(ma_sp),
                FOREIGN KEY (ma_don_hang) REFERENCES don_hang(ma_don_hang)
            )
        ''')

        # Kiểm tra xem đã có admin chưa
        cursor.execute("SELECT COUNT(*) FROM user WHERE vai_tro = 'admin'")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.execute('''
                INSERT INTO user (ma_user, ten_dang_nhap, mat_khau, ho_ten, email, vai_tro, trang_thai, ngay_tao)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', ('U001', 'admin', 'admin123', 'Quản trị viên',
                  'admin@example.com', 'admin', 'hoatdong',
                  datetime.now()))
            self._connection.commit()

        cursor.close()

    def close(self):
        """Đóng kết nối"""
        if self._connection:
            self._connection.close()
            self._connection = None


if __name__ == "__main__":
    # Khởi tạo instance DatabaseConnection
    db = DatabaseConnection()

    # Lấy connection
    conn = db.get_connection()

    # Tạo con trỏ
    cursor = conn.cursor()

    # Thực thi câu truy vấn lấy danh sách sản phẩm
    cursor.execute("SELECT * FROM san_pham")

    # Lấy dữ liệu
    rows = cursor.fetchall()

    for row in rows:
        print(dict(zip(cursor.column_names, row)))  # Chuyển row thành dict

    # Đóng cursor
    cursor.close()

    # Đóng kết nối
    db.close()
