class Brand:

    def __init__(self, brand_id: int, brand_name: str,
                 country: str = "", brand_des: str = ""):
        self.brand_id = brand_id
        self.brand_name = brand_name
        self.country = country
        self.brand_des = brand_des