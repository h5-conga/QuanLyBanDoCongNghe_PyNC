from typing import List, Tuple
from src.dao.warranty_dao import WarrantyDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.product_dao import ProductDAO


class WarrantyController:
    def __init__(self):
        self.warranty_dao = WarrantyDAO()
        self.customer_dao = CustomerDAO()
        self.product_dao = ProductDAO()

    def _format_warranties(self, warranties_list) -> List[Tuple]:
        data_view = []
        for w in warranties_list:
            customer_name = "Unknown"
            if w.customer_id:
                cust = self.customer_dao.find_by_id(w.customer_id)
                if cust:
                    customer_name = cust.customer_name
            product_name = "Unknown"
            product_code = f"SP{w.product_id}"
            if w.product_id:
                prod = self.product_dao.get_by_product_id(w.product_id)
                if prod:
                    product_name = prod.product_name

            start_str = w.start_date.strftime("%Y-%m-%d") if w.start_date else ""
            end_str = w.end_date.strftime("%Y-%m-%d") if w.end_date else ""

            row = (
                w.warranty_id,
                customer_name,
                product_code,
                product_name,
                w.phone,
                start_str,
                w.warranty_date,
                end_str
            )
            data_view.append(row)
        return data_view

    def get_all_warranties_for_view(self) -> List[Tuple]:
        warranties = self.warranty_dao.get_all()
        return self._format_warranties(warranties)

    def filter_by_status(self, status: str) -> List[Tuple]:
        all_warranties = self.warranty_dao.get_all()
        filtered = []

        for w in all_warranties:
            is_active = w.check_time()

            if status == 'all':
                filtered.append(w)
            elif status == 'active' and is_active:
                filtered.append(w)
            elif status == 'expired' and not is_active:
                filtered.append(w)

        return self._format_warranties(filtered)

    def search_warranties(self, query: str) -> List[Tuple]:
        all_data = self.get_all_warranties_for_view()
        query = query.lower().strip()

        if not query:
            return all_data

        filtered = []
        for row in all_data:
            c_name = str(row[1]).lower()
            p_name = str(row[3]).lower()
            phone = str(row[4])

            if query in c_name or query in p_name or query in phone:
                filtered.append(row)

        return filtered