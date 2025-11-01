from datetime import datetime

from src.models import Order_Detail
from typing import List

class Order:
    """Lớp đại diện cho Đơn hàng"""

    def __init__(self, order_id: str, customer_id: str, customer_name: str,
                 date: datetime, status: str = "Đang xử lý"):
        self.order_id = order_id
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.date = date
        self.status = status
        self.order_list: List[Order_Detail] = []

    def add_prodcut(self, detail: Order_Detail):
        """Thêm sản phẩm vào đơn hàng"""
        self.order_list.append(detail)

    def total_price(self) -> float:
        """Tính tổng tiền đơn hàng"""
        return sum(ct.tinh_thanh_tien() for ct in self.order_list)

    def update_status(self, new_status: str):
        """Cập nhật trạng thái đơn hàng"""
        self.status = new_status

    def __str__(self):
        return f"DH[{self.order_id}] {self.customer_name} - Tổng: {self.total_price():,.0f}đ - {self.status}"