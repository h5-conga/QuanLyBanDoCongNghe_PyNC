from datetime import datetime
from typing import List

from src.models.entity import OrderDetail


class Order:

    def __init__(self, order_id: int, customer_id: int, user_id: int,
                 date: datetime):
        self.order_id = order_id
        self.customer_id = customer_id
        self.date = date
        self.user_id = user_id
        self.order_list: List[OrderDetail] = []

    def add_product(self, detail: OrderDetail):
        self.order_list.append(detail)

    def total_price(self) -> float:
        return sum(ct.total_amount() for ct in self.order_list)

    def __str__(self):
        return f"DH[{self.order_id}] {self.customer_id} - Tổng: {self.total_price():,.0f}đ "