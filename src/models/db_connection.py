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
                port=3306,
                user='root',
                password='123123'
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute("CREATE DATABASE IF NOT EXISTS sales_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            temp_cursor.close()
            temp_conn.close()
        except Error as e:
            print(f"Lỗi khi tạo database: {e}")
            raise

    def get_connection(self):
        """Lấy kết nối đến MySQL"""
        if self._connection is None:
            try:
                self._create_database_if_not_exists()
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

        # Bảng Category
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Category (
                category_id VARCHAR(20) PRIMARY KEY,
                category_name NVARCHAR(255) NOT NULL,
                category_des TEXT
            )
        ''')

        # Bảng Brand
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Brand (
                brand_id VARCHAR(20) PRIMARY KEY,
                brand_name NVARCHAR(255) NOT NULL,
                country VARCHAR(100),
                brand_des TEXT
            )
        ''')

        # Bảng User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                user_id VARCHAR(20) PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fullname NVARCHAR(255) NOT NULL,
                role ENUM('admin','manager','cashier') DEFAULT 'cashier',
                status_user ENUM('Active','Lock') DEFAULT 'Active'
            )
        ''')

        # Bảng Product
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                product_id VARCHAR(20) PRIMARY KEY,
                product_name NVARCHAR(255) NOT NULL,
                barcode VARCHAR(100),
                price DECIMAL(15,2),
                stock_quantity INT,
                entry_date DATETIME,
                warranty_date INT,
                cost_price DECIMAL(15,2),
                brand_id VARCHAR(20),
                category_id VARCHAR(20),
                description TEXT,
                FOREIGN KEY (brand_id) REFERENCES Brand(brand_id),
                FOREIGN KEY (category_id) REFERENCES Category(category_id)
            )
        ''')

        # Bảng ProductImage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProductImage (
                image_id VARCHAR(20) PRIMARY KEY,
                product_id VARCHAR(20),
                image_url TEXT,
                image_path TEXT,
                image_alt VARCHAR(255),
                FOREIGN KEY (product_id) REFERENCES Product(product_id)
            )
        ''')

        # Bảng Customer
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
                customer_id VARCHAR(20) PRIMARY KEY,
                customer_name NVARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                email VARCHAR(255)
            )
        ''')

        # Bảng Order
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS `Order` (
                order_id VARCHAR(20) PRIMARY KEY,
                customer_id VARCHAR(20),
                user_id VARCHAR(20),
                date DATETIME,
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id),
                FOREIGN KEY (user_id) REFERENCES User(user_id)
            )
        ''')

        # Bảng Order_Detail
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Order_Detail (
                order_id VARCHAR(20),
                product_id VARCHAR(20),
                quantity INT,
                start_date DATETIME,
                PRIMARY KEY (order_id, product_id),
                FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
                FOREIGN KEY (product_id) REFERENCES Product(product_id)
            )
        ''')

        # Bảng Warranty
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Warranty (
                warranty_id VARCHAR(20) PRIMARY KEY,
                product_id VARCHAR(20),
                order_id VARCHAR(20),
                customer_id VARCHAR(20),
                phone VARCHAR(20),
                start_date DATETIME,
                warranty_date INT,
                end_date DATETIME,
                FOREIGN KEY (product_id) REFERENCES Product(product_id),
                FOREIGN KEY (order_id) REFERENCES `Order`(order_id),
                FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
            )
        ''')

        # Kiểm tra có admin chưa
        cursor.execute("SELECT COUNT(*) FROM User WHERE role = 'admin'")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute('''
                INSERT INTO User (user_id, username, password, fullname, role, status_user)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', ('U001', 'admin', 'admin123', 'Quản trị viên', 'admin', 'Active'))
            self._connection.commit()
            print(" Đã thêm tài khoản admin mặc định!")

        self._connection.commit()
        cursor.close()
        print("Các bảng đã được tạo thành công!")

    def close(self):
        """Đóng kết nối"""
        if self._connection:
            self._connection.close()
            self._connection = None


if __name__ == "__main__":
    db = DatabaseConnection()
    conn = db.get_connection()

    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    print(" Danh sách bảng trong cơ sở dữ liệu:")
    for t in cursor.fetchall():
        print(" -", t[0])
    cursor.close()

    db.close()
