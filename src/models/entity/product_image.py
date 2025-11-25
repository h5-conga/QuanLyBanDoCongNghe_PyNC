class ProductImage:
    def __init__(self, image_id: int, product_id: int, image_url: str, image_path: str,
                 image_alt: str = ""):
        self.image_id = image_id
        self.product_id = product_id
        self.image_url = image_url
        self.image_path = image_path
        self.image_alt = image_alt