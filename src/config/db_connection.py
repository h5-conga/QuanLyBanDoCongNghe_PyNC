import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _create_database_if_not_exists(self):
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
        cursor = self._connection.cursor()

        # Bảng Category
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS category (
                category_id INT PRIMARY KEY AUTO_INCREMENT,
                category_name NVARCHAR(255) NOT NULL,
                category_des TEXT
            )
        ''')

        # Bảng Brand
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brand (
                brand_id INT PRIMARY KEY AUTO_INCREMENT,
                brand_name NVARCHAR(255) NOT NULL,
                country VARCHAR(100),
                brand_des TEXT
            )
        ''')

        # Bảng User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                user_id INT PRIMARY KEY AUTO_INCREMENT,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                fullname NVARCHAR(255) NOT NULL,
                role ENUM('admin','manager','cashier') NOT NULL DEFAULT 'cashier',
                status_user ENUM('active','lock') NOT NULL DEFAULT 'active'
            )
        ''')

        # Bảng Product
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                product_name NVARCHAR(255) NOT NULL,
                price DECIMAL(15,2),
                stock_quantity INT,
                entry_date DATETIME,
                warranty_date INT,
                cost_price DECIMAL(15,2),
                brand_id INT,
                category_id INT,
                description TEXT,
                FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
                FOREIGN KEY (category_id) REFERENCES category(category_id)
            )
        ''')

        # Bảng ProductImage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS product_image (
                image_id INT PRIMARY KEY AUTO_INCREMENT,
                product_id INT,
                image_url TEXT,
                image_path TEXT,
                image_alt VARCHAR(255),
                FOREIGN KEY (product_id) REFERENCES product(product_id)
            )
        ''')

        # Bảng Customer
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customer (
                customer_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_name NVARCHAR(255) NOT NULL,
                phone VARCHAR(20),
                address TEXT,
                email VARCHAR(255)
            )
        ''')

        # Bảng Order
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order (
                order_id INT PRIMARY KEY AUTO_INCREMENT,
                customer_id INT,
                user_id INT,
                date DATETIME,
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
                FOREIGN KEY (user_id) REFERENCES user(user_id)
            )
        ''')

        # Bảng Order_Detail
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_detail (
                order_id INT,
                product_id INT,
                quantity INT,
                start_date DATETIME,
                PRIMARY KEY (order_id, product_id),
                FOREIGN KEY (order_id) REFERENCES order(order_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id)
            )
        ''')

        # Bảng Warranty
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS warranty (
                warranty_id INT PRIMARY KEY AUTO_INCREMENT,
                product_id INT,
                order_id INT,
                customer_id INT,
                phone VARCHAR(20),
                start_date DATETIME,
                warranty_date INT,
                end_date DATETIME,
                FOREIGN KEY (product_id) REFERENCES product(product_id),
                FOREIGN KEY (order_id) REFERENCES order(order_id),
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
            )
        ''')

        cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'admin'")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute('''
                INSERT INTO User (user_id, username, password, fullname, role, status_user)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (1, 'admin', 'admin', 'Quản trị viên mặc định', 'admin', 'active'))
            self._connection.commit()
            print(" Đã thêm tài khoản admin mặc định!")

        self._connection.commit()
        cursor.close()
        print("Các bảng đã được tạo thành công!")

    def close(self):
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
