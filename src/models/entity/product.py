from datetime import datetime

class Product:
    def __init__(self, product_id: int,image_id: int, product_name: str, price: float,
                 stock_quantity: int, entry_date: datetime, warranty_date: int, cost_price: float,
                 brand_id: int, category_id: int, description: str = ""):
        self.product_id = product_id
        self.image_id = image_id
        self.product_name = product_name
        self.price = price
        self.stock_quantity = stock_quantity
        self.entry_date = entry_date
        self.warranty_date = warranty_date #unit: month
        self.description = description
        self.brand_id = brand_id
        self.category_id = category_id
        self.cost_price = cost_price

    def out_stock(self, value: int = 10) -> bool:
        return self.stock_quantity <= value

    def stock_value(self) -> float:
        return self.cost_price * self.stock_quantity
