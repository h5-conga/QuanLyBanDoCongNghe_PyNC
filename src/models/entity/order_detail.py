from datetime import datetime
from src.models.entity import Product


class OrderDetail:

    def __init__(self, product: Product, quantity: int, start_date: datetime):
        self.quantity = quantity
        self.product = product
        self.start_date = start_date
        self.unit_price = product.price
        self.total_amount = self.quantity * self.unit_price