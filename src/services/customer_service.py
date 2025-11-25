from typing import List, Optional
from src.models.entity import Customer
from src.dao.customer_dao import CustomerDAO


class CustomerService:
    def __init__(self):
        self.customer_dao = CustomerDAO()

    def add_customer(self, customer_name: str, phone: str, address: str, email: str) -> Optional[Customer]:
        if not customer_name.strip():
            print("Tên khách hàng không được để trống.")
            return None
        if not phone.strip():
            print("Số điện thoại không được để trống.")
            return None
        new_customer = Customer(
            customer_id=None,
            customer_name=customer_name,
            phone=phone,
            address=address,
            email=email
        )
        return self.customer_dao.add_customer(new_customer)

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self.customer_dao.find_by_id(customer_id)

    def get_customer_by_phone(self, phone: str) -> Optional[Customer]:
        return self.customer_dao.find_by_phone(phone)

    def list_all_customers(self) -> List[Customer]:
        return self.customer_dao.list_all_customers()

    def search_customers(self, keyword: str) -> List[Customer]:
        if not keyword.strip():
            return []
        return self.customer_dao.search_by_name_or_phone(keyword)
