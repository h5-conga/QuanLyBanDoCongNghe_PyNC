from datetime import datetime

from src.models.entity import Product


class OrderDetail:

    def __init__(self, product: Product, quantity: int, start_date: datetime):
        self.quantity = quantity
        self.product = product
        self.start_date = start_date

    def total_amount(self) -> float:
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.product_name} x{self.quantity} = {self.total_amount():,.0f}đ"