import tkinter as tk
from tkinter import ttk, messagebox
import re
from src.controllers.order_controller import OrderController
from src.controllers.customer_controller import CustomerController
from src.views.add_customer_view import AddCustomerView


class AddOrderView(tk.Toplevel):
    def __init__(self, parent, current_user_id=None, callback_success=None):
        super().__init__(parent)
        self.title("Tạo Hóa Đơn Mới")
        self.geometry("1000x650")
        self.configure(bg="#f5f5f5")
        self.callback_success = callback_success
        self.controller = OrderController()
        self.customer_controller = CustomerController()
        self.logged_in_user = None
        if hasattr(parent, 'current_user') and parent.current_user:
            self.logged_in_user = parent.current_user
        elif hasattr(parent, 'master') and hasattr(parent.master, 'current_user'):
            self.logged_in_user = parent.master.current_user
        self.current_user_id = current_user_id
        if self.logged_in_user:
            self.current_user_id = self.logged_in_user.user_id
        self.cart_data = []
        self.customers = []
        self.products = []
        self.customer_values = []
        self.product_values = []
        self.selected_product = None
        self.selected_customer_id = None
        self.create_widgets()
        self.load_combobox_data()

    def create_widgets(self):
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)
        left_frame = tk.Frame(self, bg="white", padx=15, pady=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        tk.Label(left_frame, text="THÔNG TIN ĐƠN HÀNG", font=("Arial", 12, "bold"), bg="white", fg="#2196F3").pack(
            anchor="w", pady=(0, 10))
        staff_name = "Admin/Không xác định"
        if self.logged_in_user:
            staff_name = getattr(self.logged_in_user, 'fullname', self.logged_in_user.username)

        tk.Label(left_frame, text=f"Nhân viên tạo: {staff_name}",
                 font=("Arial", 10, "italic"), fg="#555", bg="white").pack(anchor="w", pady=(0, 15))
        tk.Label(left_frame, text="Khách hàng:", bg="white", font=("Arial", 10, "bold")).pack(
            anchor="w")

        cust_frame = tk.Frame(left_frame, bg="white")
        cust_frame.pack(fill="x", pady=(5, 15))
        self.cb_customer = ttk.Combobox(cust_frame, height=10)
        self.cb_customer.pack(side=tk.LEFT, fill="x", expand=True)
        self.cb_customer.bind('<KeyRelease>', self.on_customer_search)  # Sự kiện gõ phím
        self.cb_customer.bind("<<ComboboxSelected>>", self.on_customer_select)
        btn_add_cust = tk.Button(cust_frame, text="+", bg="#4CAF50", fg="white",
                                 font=("Arial", 10, "bold"), bd=0, padx=10,
                                 command=self.open_add_customer_popup)
        btn_add_cust.pack(side=tk.RIGHT, padx=(5, 0))

        ttk.Separator(left_frame, orient="horizontal").pack(fill="x", pady=10)
        tk.Label(left_frame, text="Chọn sản phẩm:", bg="white", font=("Arial", 10, "bold")).pack(
            anchor="w")
        self.cb_product = ttk.Combobox(left_frame, height=15)
        self.cb_product.pack(fill="x", pady=(5, 5))
        self.cb_product.bind('<KeyRelease>', self.on_product_search)  # Sự kiện gõ phím
        self.cb_product.bind("<<ComboboxSelected>>", self.on_product_select)
        self.lbl_product_info = tk.Label(left_frame, text="Giá: 0 đ | Tồn: 0", bg="#f9f9f9", fg="#666", anchor="w",
                                         padx=5)
        self.lbl_product_info.pack(fill="x", pady=(0, 10))
        tk.Label(left_frame, text="Số lượng:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
        self.spin_qty = tk.Spinbox(left_frame, from_=1, to=100, width=10, font=("Arial", 11))
        self.spin_qty.pack(anchor="w", pady=(5, 15))
        btn_add = tk.Button(left_frame, text="Thêm vào giỏ >>", bg="#FF9800", fg="white",
                            font=("Arial", 10, "bold"), bd=0, padx=10, pady=8,
                            command=self.add_to_cart)
        btn_add.pack(fill="x")
        right_frame = tk.Frame(self, bg="white", padx=15, pady=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        tk.Label(right_frame, text="GIỎ HÀNG", font=("Arial", 12, "bold"), bg="white", fg="#4CAF50").pack(anchor="w",
                                                                                                          pady=(0, 10))
        cols = ("ID", "Tên SP", "Giá", "SL", "Thành Tiền")
        self.tree = ttk.Treeview(right_frame, columns=cols, show="headings")
        self.tree.heading("ID", text="ID");
        self.tree.column("ID", width=40, anchor="center")
        self.tree.heading("Tên SP", text="Tên SP");
        self.tree.column("Tên SP", width=200)
        self.tree.heading("Giá", text="Giá");
        self.tree.column("Giá", width=80, anchor="e")
        self.tree.heading("SL", text="SL");
        self.tree.column("SL", width=50, anchor="center")
        self.tree.heading("Thành Tiền", text="Thành Tiền");
        self.tree.column("Thành Tiền", width=100, anchor="e")
        self.tree.pack(fill="both", expand=True)
        btn_remove = tk.Button(right_frame, text="Xóa món đã chọn", bg="#ffcccc", fg="red", bd=0,
                               command=self.remove_from_cart)
        btn_remove.pack(anchor="e", pady=5)
        ttk.Separator(right_frame, orient="horizontal").pack(fill="x", pady=10)
        total_frame = tk.Frame(right_frame, bg="white")
        total_frame.pack(fill="x")
        tk.Label(total_frame, text="TỔNG CỘNG:", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        self.lbl_total = tk.Label(total_frame, text="0 VNĐ", font=("Arial", 16, "bold"), bg="white", fg="#d32f2f")
        self.lbl_total.pack(side="right")
        self.btn_save = tk.Button(right_frame, text="LƯU ĐƠN HÀNG", bg="#2196F3", fg="white",
                                  font=("Arial", 12, "bold"), bd=0, pady=12,
                                  command=self.save_order)
        self.btn_save.pack(fill="x", pady=(20, 0))
    def load_combobox_data(self):
        self.customers = self.controller.get_all_customers()
        self.customer_values = [f"{c['id']} - {c['name']} ({c['phone']})" for c in self.customers]
        self.cb_customer['values'] = self.customer_values
        self.products = self.controller.get_all_products_for_selection()
        self.product_values = [f"{p['id']} - {p['name']}" for p in self.products]
        self.cb_product['values'] = self.product_values

    def on_customer_search(self, event):
        value = event.widget.get()
        if value == '':
            self.cb_customer['values'] = self.customer_values
        else:
            data = []
            for item in self.customer_values:
                if value.lower() in item.lower():
                    data.append(item)
            self.cb_customer['values'] = data

    def on_customer_select(self, event):
        selected_str = self.cb_customer.get()
        match = re.match(r"^(\d+)\s-", selected_str)
        if match:
            self.selected_customer_id = int(match.group(1))

    def on_product_search(self, event):
        value = event.widget.get()
        if value == '':
            self.cb_product['values'] = self.product_values
        else:
            data = []
            for item in self.product_values:
                if value.lower() in item.lower():
                    data.append(item)
            self.cb_product['values'] = data

    def on_product_select(self, event):
        selected_str = self.cb_product.get()
        match = re.match(r"^(\d+)\s-", selected_str)

        if match:
            p_id = int(match.group(1))
            for p in self.products:
                if p['id'] == p_id:
                    self.selected_product = p
                    price = p['price']
                    stock = p['stock']

                    self.lbl_product_info.config(text=f"Giá: {price:,.0f} đ  |  Tồn kho: {stock}")
                    if stock > 0:
                        self.spin_qty.config(to=stock, state="normal")
                        self.spin_qty.delete(0, "end")
                        self.spin_qty.insert(0, 1)
                    else:
                        self.spin_qty.config(state="disabled")
                    return
        self.selected_product = None
        self.lbl_product_info.config(text="Giá: 0 đ | Tồn: 0")

    def open_add_customer_popup(self):
        AddCustomerView(self, self.customer_controller, self.refresh_customers_after_add)

    def refresh_customers_after_add(self):
        self.customers = self.controller.get_all_customers()
        self.customer_values = [f"{c['id']} - {c['name']} ({c['phone']})" for c in self.customers]
        self.cb_customer['values'] = self.customer_values
        if self.customers:
            newest_customer = max(self.customers, key=lambda x: x['id'])
            value_str = f"{newest_customer['id']} - {newest_customer['name']} ({newest_customer['phone']})"
            self.cb_customer.set(value_str)
            self.selected_customer_id = newest_customer['id']
            messagebox.showinfo("Thông báo", f"Đã chọn khách hàng mới: {newest_customer['name']}")

    def add_to_cart(self):
        if not self.selected_product:
            self.on_product_select(None)
            if not self.selected_product:
                messagebox.showwarning("Cảnh báo", "Vui lòng chọn sản phẩm hợp lệ!")
                return
        try:
            qty = int(self.spin_qty.get())
            if qty <= 0: raise ValueError
        except ValueError:
            messagebox.showwarning("Lỗi", "Số lượng phải là số dương!")
            return
        if qty > self.selected_product['stock']:
            messagebox.showerror("Hết hàng",
                                 f"Tồn kho chỉ còn {self.selected_product['stock']} sản phẩm. Không thể thêm {qty}.")
            self.spin_qty.delete(0, "end")
            self.spin_qty.insert(0, self.selected_product['stock'])
            return

        current_qty_in_cart = 0
        for item in self.cart_data:
            if item['id'] == self.selected_product['id']:
                current_qty_in_cart = item['quantity']
                break

        if current_qty_in_cart + qty > self.selected_product['stock']:
            messagebox.showwarning("Kho",
                                   f"Trong giỏ đã có {current_qty_in_cart}. Tổng quá tồn kho ({self.selected_product['stock']})!")
            return

        found = False
        for item in self.cart_data:
            if item['id'] == self.selected_product['id']:
                item['quantity'] += qty
                item['total'] = item['quantity'] * item['price']
                found = True
                break

        if not found:
            item = {
                "id": self.selected_product['id'],
                "name": self.selected_product['name'],
                "price": self.selected_product['price'],
                "quantity": qty,
                "total": qty * self.selected_product['price']
            }
            self.cart_data.append(item)

        self.refresh_cart_ui()

    def remove_from_cart(self):
        selected = self.tree.selection()
        if not selected: return
        row_values = self.tree.item(selected[0])['values']
        p_id = row_values[0]
        self.cart_data = [i for i in self.cart_data if i['id'] != p_id]
        self.refresh_cart_ui()

    def refresh_cart_ui(self):
        self.tree.delete(*self.tree.get_children())
        total_bill = 0
        for item in self.cart_data:
            self.tree.insert("", "end", values=(
                item['id'], item['name'],
                f"{item['price']:,.0f}", item['quantity'],
                f"{item['total']:,.0f}"
            ))
            total_bill += item['total']
        self.lbl_total.config(text=f"{total_bill:,.0f} VNĐ")

    def save_order(self):
        if not self.cart_data:
            messagebox.showwarning("Trống", "Giỏ hàng đang trống!")
            return
        if not self.selected_customer_id:
            self.on_customer_select(None)

        if not self.selected_customer_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn khách hàng từ danh sách!")
            return
        cust_name = "Khách hàng"
        for c in self.customers:
            if c['id'] == self.selected_customer_id:
                cust_name = c['name']
                break

        user_id = self.logged_in_user.user_id if self.logged_in_user else (self.current_user_id or 1)
        if messagebox.askyesno("Xác nhận", f"Lưu đơn hàng cho khách: {cust_name}?"):
            self.btn_save.config(state=tk.DISABLED, text="Đang lưu...")
            self.update_idletasks()
            success = self.controller.create_full_order(self.selected_customer_id, user_id, self.cart_data)
            if success:
                messagebox.showinfo("Thành công", "Đã tạo hóa đơn thành công!")
                if self.callback_success:
                    self.callback_success()
                self.destroy()
            else:
                messagebox.showerror("Lỗi", "Có lỗi xảy ra khi lưu đơn hàng.")
                self.btn_save.config(state=tk.NORMAL, text="LƯU ĐƠN HÀNG")