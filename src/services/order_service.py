from typing import List, Optional
from datetime import datetime
from src.models.entity import Order
from src.dao.order_dao import OrderDAO


class OrderService:
    def __init__(self):
        self.order_dao = OrderDAO()

    def create_order(self, customer_id: int, user_id: int, date: Optional[datetime] = None) -> Optional[Order]:
        if date is None:
            date = datetime.now()
        new_order = Order(order_id=None, customer_id=customer_id, user_id=user_id, date=date)
        return self.order_dao.add_order(new_order)

    def update_order(self, order_id: int, customer_id: int, user_id: int, date: Optional[datetime] = None) -> bool:
        if date is None:
            date = datetime.now()
        return self.order_dao.update_order(order_id, customer_id, user_id, date)

    def delete_order(self, order_id: int) -> bool:
        return self.order_dao.delete_order(order_id)

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.order_dao.find_by_id(order_id)

    def get_all_orders(self) -> List[Order]:
        return self.order_dao.list_all_orders()

    def get_orders_by_customer_id(self, customer_id: int) -> List[Order]:
        return self.order_dao.find_by_customer_id(customer_id)

    def get_orders_by_customer_name(self, customer_name: str) -> List[Order]:
        return self.order_dao.find_by_customer_name(customer_name)
