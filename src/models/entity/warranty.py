from datetime import datetime
from dateutil.relativedelta import relativedelta


class Warranty:

    def __init__(self, warranty_id: int, product_id: int, order_id: int, customer_id: int, phone: str,
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