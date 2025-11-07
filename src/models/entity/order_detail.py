from datetime import datetime


class Order_Detail:

    def __init__(self, product_id: int, quantity: int, start_date: datetime):
        self.product_id = product_id
        self.quantity = quantity
        self.start_date = start_date

    def total_amount(self) -> float:
        pass
        # return self.quantity * Product.price

    def __str__(self):
        return f"{self.product_id} x{self.quantity} = {self.total_amount():,.0f}đ"