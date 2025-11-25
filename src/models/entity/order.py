from datetime import datetime
from typing import List

from .order_detail import OrderDetail


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