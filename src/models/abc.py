from datetime import datetime

class Brand:

    def __init__(self, brand_id: str, brand_name: str,
                 country: str = "", brand_des: str = ""):
        self.brand_id = brand_id
        self.brand_name = brand_name
        self.country = country
        self.brand_des = brand_des

    def __str__(self):
        return f"TH[{self.brand_id}] {self.brand_name} ({self.country})"

class ProductImage:
    def __init__(self, image_id: str, product_id: str, image_url: str, image_path: str,
                 image_alt: str = ""):
        self.image_id = image_id
        self.product_id = product_id
        self.image_url = image_url  # URL hình ảnh (có thể là đường dẫn trên web)
        self.image_path = image_path  # Đường dẫn lưu trữ hình ảnh trong hệ thống file
        self.image_alt = image_alt  # Mô tả thay thế cho hình ảnh

    def __str__(self):
        # Cung cấp thông tin cơ bản về hình ảnh
        return f"Image[{self.image_id}] for Product[{self.product_id}] - {self.image_url} - {self.image_alt}"


class Product:
    def __init__(self, product_id: str,image_id: str, product_name: str, barcode: str, price: float,
                 stock_quantity: int, entry_date: datetime, warranty_date: int, cost_price: float,
                 brand_id: str, category_id: str, description: str = ""):
        self.product_id = product_id
        self.image_id = image_id
        self.product_name = product_name
        self.price = price
        self.stock_quantity = stock_quantity
        self.entry_date = entry_date
        self.warranty_date = warranty_date #unit: month
        self.description = description
        self.brand_id = brand_id
        self.category_id = category_id
        self.cost_price = cost_price

    def out_stock(self, value: int = 10) -> bool:
        return self.stock_quantity <= value

    def stock_value(self) -> float:
        return self.cost_price * self.stock_quantity

    def __str__(self):
        return f"SP[{self.product_id}] {self.product_name} - Giá: {self.price:,.0f}đ - Tồn: {self.stock_quantity}"

class User:

    def __init__(self, user_id: str, username: str, password: str,
                 fullname: str, role: str,
                 status_user: str = "Active"):
        self.user_id = user_id
        self.username = username
        self.password = password  # Nên mã hóa trong thực tế
        self.fullname = fullname
        self.role = role  # admin, manager, cashier
        self.status_user = status_user  # active, loc

    def check_password(self, password: str) -> bool:
        return self.password == password

    def check_admin(self) -> bool:
        return self.role == "admin"

    def check_manager(self) -> bool:
        return self.role == "manager"

    def check_cashier(self) -> bool:
        return self.role == "cashier"

    def __str__(self):
        return f"User[{self.username}] {self.fullname} - {self.role}"


class Order_Detail:

    def __init__(self, product_id: str, quantity: int, start_date: datetime):
        self.product_id = product_id
        self.quantity = quantity
        self.start_date = start_date

    def total_amount(self) -> float:
        pass
        # return self.quantity * Product.price

    def __str__(self):
        return f"{self.product_id} x{self.quantity} = {self.total_amount():,.0f}đ"

from typing import List

class Order:

    def __init__(self, order_id: str, customer_id: str, user_id: str,
                 date: datetime):
        self.order_id = order_id
        self.customer_id = customer_id
        self.date = date
        self.user_id = user_id
        self.order_list: List[Order_Detail] = []

    def add_product(self, detail: Order_Detail):
        self.order_list.append(detail)

    def total_price(self) -> float:
        return sum(ct.total_amount() for ct in self.order_list)

    def __str__(self):
        return f"DH[{self.order_id}] {self.customer_id} - Tổng: {self.total_price():,.0f}đ "


class Customer:

    def __init__(self, customer_id: str, customer_name: str, phone: str,
                 address: str = "", email: str = ""):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.email = email

    def __str__(self):
        return f"KH[{self.customer_id}] {self.customer_name} - SĐT: {self.phone}"

class Category:

    def __init__(self, category_id: str, category_name: str, category_des: str = ""):
        self.category_id = category_id
        self.category_name = category_name
        self.category_des = category_des

    def __str__(self):
        return f"DM[{self.category_id}] {self.category_name}"

from dateutil.relativedelta import relativedelta

class Warranty:

    def __init__(self, warranty_id: str, product_id: str, order_id: str, customer_id: str, phone: str,
                 start_date: datetime, warranty_date: int):
        self.warranty_id = warranty_id
        self.product_id = product_id
        self.order_id = order_id
        self.customer_id = customer_id
        self.phone = phone
        self.start_date = start_date
        self.warranty_date = warranty_date

        self.end_date = self.start_date + relativedelta(months=self.warranty_date)

    def check_time(self) -> bool:
        return datetime.now() <= self.end_date