from datetime import datetime

class Product:
    def __init__(self, product_id: str, product_name: str, category: str, price: float,
                 stock_quantity: int, entry_date: datetime, warranty_date: int,
                 description: str = "", supplier: str = ""):
        self.product_id = product_id
        self.product_name = product_name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity
        self.entry_date = entry_date
        self.warranty_date = warranty_date #unit: month
        self.description = description
        self.supplier = supplier

    def out_stock(self, value: int = 10) -> bool:
        return self.stock_quantity <= value

    def stock_value(self) -> float:
        return self.price * self.stock_quantity

    def __str__(self):
        return f"SP[{self.product_id}] {self.product_name} - Giá: {self.price:,.0f}đ - Tồn: {self.stock_quantity}"