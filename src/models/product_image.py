class ProductImage:
    def __init__(self, image_id: str, product_id: str, image_url: str, image_path: str,
                 image_alt: str = ""):
        self.image_id = image_id
        self.product_id = product_id
        self.image_url = image_url  # URL hình ảnh (có thể là đường dẫn trên web)
        self.image_path = image_path  # Đường dẫn lưu trữ hình ảnh trong hệ thống file
        self.image_alt = image_alt  # Mô tả thay thế cho hình ảnh

    def __str__(self):
        # Cung cấp thông tin cơ bản về hình ảnh
        return f"Image[{self.image_id}] for Product[{self.product_id}] - {self.image_url} - {self.image_alt}"