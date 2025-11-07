class Category:

    def __init__(self, category_id: int, category_name: str, category_des: str = ""):
        self.category_id = category_id
        self.category_name = category_name
        self.category_des = category_des

    def __str__(self):
        return f"DM[{self.category_id}] {self.category_name}"