from datetime import datetime # Đưa datetime lên đầu cùng với các imports khác
from typing import List

from QuanLyBanDoCongNghe_PyNC.src.models.entity import OrderDetail


# Loại bỏ dòng import sai cú pháp trước đó

# (Loại bỏ dòng 'from src.models.entity import OrderDetail' ở đây nếu không cần thiết
# vì bạn đã import nó từ '.' ở trên)

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