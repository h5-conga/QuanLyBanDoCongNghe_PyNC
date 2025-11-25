class Customer:

    def __init__(self, customer_id: int, customer_name: str, phone: str,
                 address: str = "", email: str = ""):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.phone = phone
        self.address = address
        self.email = email
