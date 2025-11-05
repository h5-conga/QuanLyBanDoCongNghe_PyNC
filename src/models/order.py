from datetime import datetime

from src.models import Order_Detail
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