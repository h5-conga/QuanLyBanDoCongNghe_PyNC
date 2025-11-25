import tkinter as tk
from src.views.customer_view import CustomerView
from src.views.product_view import ProductView
from src.views.order_view import OrderView
from src.views.statistic_view import StatisticsView
from src.views.warranty_view import WarrantyView
from src.views.account_view import AccountView


class MainView(tk.Tk):
    def __init__(self, current_user):
        super().__init__()
        self.title(f"Hệ thống Quản lý Bán hàng - Xin chào: {current_user.fullname}")
        self.geometry("1200x700")
        self.state('zoomed')
        self.configure(bg="#f0f0f0")
        self.current_user = current_user
        self.role = current_user.role
        self.current_user_id = current_user.user_id
        self.container = tk.Frame(self, bg="#f0f0f0")
        self.container.pack(fill="both", expand=True)
        self.switch_view("Sản phẩm")

    def switch_view(self, view_name):
        for widget in self.container.winfo_children():
            widget.destroy()

        new_view = None
        if view_name == "Sản phẩm":
            new_view = ProductView(master=self.container, role=self.role)

        elif view_name == "Đơn hàng":
            new_view = OrderView(master=self.container, role=self.role)

        elif view_name == "Bảo hành":
            new_view = WarrantyView(master=self.container, role=self.role)

        elif view_name == "Khách hàng":
            new_view = CustomerView(master=self.container, role=self.role)

        elif view_name == "Thống kê":
            new_view = StatisticsView(master=self.container, role=self.role)

        elif view_name == "Tài khoản":
            new_view = AccountView(master=self.container)

        if new_view:
            new_view.pack(fill="both", expand=True)
            new_view.main_controller = self