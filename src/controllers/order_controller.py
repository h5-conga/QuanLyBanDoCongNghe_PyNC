from typing import List, Dict
from datetime import datetime
from src.services.order_service import OrderService
from src.dao.order_detail_dao import OrderDetailDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.product_dao import ProductDAO
from src.dao.warranty_dao import WarrantyDAO
from src.dao.user_dao import UserDAO
from src.models.entity import OrderDetail, Warranty


class OrderController:
    def __init__(self):
        self.order_service = OrderService()
        self.detail_dao = OrderDetailDAO()
        self.customer_dao = CustomerDAO()
        self.product_dao = ProductDAO()
        self.warranty_dao = WarrantyDAO()
        self.user_dao = UserDAO()

    def get_all_orders_view(self) -> List[Dict]:
        orders = self.order_service.get_all_orders()
        view_data = []
        for order in orders:
            customer_name = "Unknown"
            if order.customer_id:
                cust = self.customer_dao.find_by_id(order.customer_id)
                if cust: customer_name = cust.customer_name
            staff_name = f"ID: {order.user_id}"
            if order.user_id:
                try:
                    staff_user = self.user_dao.find_userid(order.user_id)
                    if staff_user:
                        staff_name = getattr(staff_user, 'fullname', staff_user.username)
                except Exception:
                    pass
            details = self.detail_dao.get_order_details_by_order_id(order.order_id)
            total_money = sum(getattr(d, 'total_price', 0) for d in details)

            view_data.append({
                "id": order.order_id,
                "customer_name": customer_name,
                "date": order.date,
                "total": total_money,
                "user_id": order.user_id,
                "staff_name": staff_name
            })
        return view_data

    def get_order_details(self, order_id: int) -> Dict:
        order = self.order_service.get_order_by_id(order_id)
        if not order: return None

        customer_name = "Khách lẻ"
        if order.customer_id:
            cust = self.customer_dao.find_by_id(order.customer_id)
            if cust: customer_name = cust.customer_name

        staff_name = f"Mã {order.user_id}"
        if order.user_id:
            try:
                staff = self.user_dao.find_userid(order.user_id)
                if staff:
                    staff_name = getattr(staff, 'fullname', staff.username)
            except Exception as e:
                print(f"Lỗi lấy thông tin nhân viên: {e}")

        details = self.detail_dao.get_order_details_by_order_id(order_id)

        return {
            "order_info": order,
            "customer_name": customer_name,
            "products": details,
            "staff_name": staff_name
        }

    def search_orders(self, keyword: str) -> List[Dict]:
        all_data = self.get_all_orders_view()
        if not keyword: return all_data
        keyword = keyword.lower()
        return [item for item in all_data if keyword in item['customer_name'].lower() or keyword in str(item['id'])]

    def get_all_customers(self) -> List[Dict]:
        customers = self.customer_dao.get_all_customers()
        return [{"id": c.customer_id, "name": c.customer_name, "phone": c.phone} for c in customers]

    def get_all_products_for_selection(self) -> List[Dict]:
        products = self.product_dao.list_products()
        return [{"id": p.product_id, "name": p.product_name, "price": p.price, "stock": p.stock_quantity}
                for p in products if p.stock_quantity > 0]

    def create_full_order(self, customer_id: int, user_id: int, cart_items: List[Dict]) -> bool:
        new_order = self.order_service.create_order(customer_id, user_id)
        if not new_order: return False

        customer = self.customer_dao.find_by_id(customer_id)
        customer_phone = customer.phone if customer else ""

        for item in cart_items:
            product_id = item['id']
            quantity = item['quantity']

            product = self.product_dao.get_by_product_id(product_id)
            if not product: continue

            detail = OrderDetail(product, quantity, datetime.now())
            self.detail_dao.add_order_detail(detail, new_order.order_id)

            product.stock_quantity -= quantity
            self.product_dao.update_product(product)

            if product.warranty_date and product.warranty_date > 0:
                try:
                    new_warranty = Warranty(
                        warranty_id=None,
                        product_id=product.product_id,
                        order_id=new_order.order_id,
                        customer_id=customer_id,
                        phone=customer_phone,
                        start_date=datetime.now(),
                        warranty_date=product.warranty_date
                    )
                    self.warranty_dao.add_warranty(new_warranty)
                except Exception as e:
                    print(f"Lỗi tạo bảo hành: {e}")

        return True