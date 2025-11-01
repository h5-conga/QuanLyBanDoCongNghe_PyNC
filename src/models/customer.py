class Customer:

    def __init__(self, customer_id: str, customer_name: str, phone: str,
                 address: str = "", email: str = ""):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.email = email

    def __str__(self):
        return f"KH[{self.customer_id}] {self.customer_name} - SĐT: {self.phone}"