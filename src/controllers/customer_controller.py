from typing import List, Tuple
from src.dao.customer_dao import CustomerDAO
from src.models.entity import Customer


class CustomerController:
    def __init__(self):
        self.customer_dao = CustomerDAO()
        self.view = None

    def set_view(self, view):
        self.view = view

    def _format_data(self, customer: Customer) -> tuple:
        ma_kh = f"{customer.customer_id}" if customer.customer_id else "N/A"

        dia_chi = customer.address if customer.address else "Chưa cập nhật"
        email = customer.email if customer.email else "Không có"

        return (
            ma_kh,
            customer.customer_name,
            dia_chi,
            customer.phone,
            email
        )

    def get_all_customers_for_view(self) -> List[tuple]:
        customers = self.customer_dao.get_all_customers()
        return [self._format_data(c) for c in customers]

    def search_customers(self, keyword: str) -> List[tuple]:
        customers = self.customer_dao.search_customers(keyword)
        return [self._format_data(c) for c in customers]

    def handle_add_customer(self, name: str, phone: str, email: str, address: str) -> Tuple[bool, str]:
        if not name:
            return False, "Tên khách hàng không được để trống."

        new_customer = Customer(
            customer_id=0,
            customer_name=name,
            phone=phone,
            address=address,
            email=email
        )

        if self.customer_dao.add_customer(new_customer):
            return True, f"Thêm thành công khách hàng: {name}"
        else:
            return False, "Lỗi khi lưu vào cơ sở dữ liệu."