import tkinter as tk
from tkinter import ttk, messagebox
import math
from src.controllers.order_controller import OrderController
from src.views.add_order_view import AddOrderView
from src.utils.menu_helper import handle_logout, handle_open_account, handle_check_inventory


class OrderView(tk.Frame):
    def __init__(self, master=None, role=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.controller = OrderController()
        self.pack(fill=tk.BOTH, expand=True)
        self.role = role if role else 'user'
        self.main_controller = None
        self.header_font = ("Arial", 14, "bold")
        self.filter_label = None
        self.current_data = []
        self.current_page = 1
        self.items_per_page = 20
        self.total_pages = 1

        self.BG_CARD = "#ffffff"
        self.TEXT_SECONDARY = "#666666"
        self.setup_styles()

        self.create_widgets()
        self.load_data()
        self.master.bind_all("<Button-1>", self.on_click_anywhere, add="+")

    def create_widgets(self):
        header_frame = tk.Frame(self, height=50, bg="#005aae")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header_frame, text="TechStore Management", bg="#005aae", fg="white", font=self.header_font).pack(side=tk.LEFT, padx=15)

        self.btn_menu = tk.Button(header_frame, text="☰", bg="#005aae", fg="white", bd=0,
                                  font=("Arial", 12, "bold"), activebackground="#45a049",
                                  command=self.show_menu_popup)
        self.btn_menu.pack(side=tk.RIGHT, padx=15)
        menu_frame = tk.Frame(self, height=40, bg="#e0e0e0")
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        menu_items = ["Sản phẩm", "Bảo hành", "Đơn hàng", "Khách hàng", "Thống kê"]

        for item in menu_items:
            btn_bg = "#c0c0c0" if item == "Đơn hàng" else "#e0e0e0"  # Tô đậm nút Đơn hàng
            btn = tk.Button(menu_frame, text=item, bg=btn_bg, fg="#333", bd=0,
                            padx=15, pady=5, activebackground="#d0d0d0")
            btn.pack(side=tk.LEFT, padx=5)

            def on_click(view_name=item):
                if hasattr(self, 'main_controller') and self.main_controller:
                    self.main_controller.switch_view(view_name)

            btn.config(command=on_click)

        footer_frame = tk.Frame(self, bg="#005aae")
        footer_frame.pack(side="bottom", fill="x")
        tk.Label(footer_frame, text="Design by Nhóm 14!", fg="white", bg="#005aae",
                 font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=10)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(main_frame, bg="#f9f9f9", height=50)
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top_frame.grid_columnconfigure(1, weight=1)

        tk.Label(top_frame, text="Đơn Hàng", bg="#f9f9f9", font=self.header_font).grid(row=0, column=0, sticky="w",
                                                                                       padx=15)

        self.search_entry = tk.Entry(top_frame, bd=0, highlightthickness=1, highlightbackground="#ccc", relief=tk.FLAT,
                                     width=30)
        self.search_entry.grid(row=0, column=1, sticky="e", padx=(5, 5))
        self.search_entry.bind("<Return>", self.on_search_enter)

        self.search_button = tk.Button(top_frame, text="Tìm", bg="#4CAF50", fg="white", bd=0, padx=12, pady=5,
                                       relief=tk.FLAT, command=self.on_search_button_click)
        self.search_button.grid(row=0, column=2, sticky="e", padx=(0, 5))

        self.create_invoice_button = tk.Button(top_frame, text="Tạo Hóa Đơn", bg="#2196F3", fg="white", bd=0, padx=12,
                                               pady=5, relief=tk.FLAT, command=self.create_invoice)
        self.create_invoice_button.grid(row=0, column=3, sticky="e", padx=(0, 10))

        self.filter_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.grid(row=2, column=0, sticky="nsew")

        columns = ("#", "Khách hàng", "ID ĐH", "Ngày đặt", "Người tạo", "Tổng tiền")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Custom.Treeview")
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background=self.BG_CARD)

        for col in columns:
            self.tree.heading(col, text=col)
            if col == "#":
                self.tree.column(col, width=40, anchor=tk.CENTER)
            elif col in ("ID ĐH", "Tổng tiền", "Ngày đặt"):
                self.tree.column(col, width=100, anchor=tk.CENTER)
            elif col == "Người tạo":
                self.tree.column(col, width=150, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=180, anchor=tk.W)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.on_order_double_click)

        pagination_frame = tk.Frame(main_frame, bg="#f0f0f0")
        pagination_frame.grid(row=3, column=0, sticky="ew", pady=5)
        self.btn_next = tk.Button(pagination_frame, text=">", command=self.next_page, bd=0, relief="solid")
        self.btn_next.pack(side=tk.RIGHT, padx=5)
        self.lbl_page_info = tk.Label(pagination_frame, text="Trang 1 / 1", bg="#f0f0f0", font=("Arial", 10))
        self.lbl_page_info.pack(side=tk.RIGHT, padx=10)
        self.btn_prev = tk.Button(pagination_frame, text="<", command=self.prev_page, bd=0, relief="solid")
        self.btn_prev.pack(side=tk.RIGHT, padx=5)

    def render_treeview(self):
        self.tree.delete(*self.tree.get_children())
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_items = self.current_data[start_index:end_index]
        for i, item in enumerate(page_items):
            creator = item.get('staff_name', item['user_id'])
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=(
                start_index + i + 1,
                item['customer_name'],
                item['id'],
                item['date'],
                creator,
                f"{item['total']:,} đ"
            ), tags=(tag,))

        self.total_pages = math.ceil(len(self.current_data) / self.items_per_page)
        if self.total_pages == 0: self.total_pages = 1
        self.lbl_page_info.config(text=f"Trang {self.current_page} / {self.total_pages}")
        self.btn_prev.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)

    def update_data_source(self, new_data):
        self.current_data = new_data
        self.current_page = 1
        self.render_treeview()

    def prev_page(self):
        if self.current_page > 1: self.current_page -= 1; self.render_treeview()

    def next_page(self):
        if self.current_page < self.total_pages: self.current_page += 1; self.render_treeview()

    def load_data(self):
        data = self.controller.get_all_orders_view()
        self.update_data_source(data)

    def on_click_anywhere(self, event):
        try:
            if not self.tree.winfo_exists(): return
        except Exception:
            return
        if not str(event.widget).startswith(str(self.tree)) and self.tree.selection():
            self.tree.selection_remove(*self.tree.selection())

    def on_search_enter(self, event):
        self.perform_search()

    def on_search_button_click(self):
        self.perform_search()

    def perform_search(self):
        query = self.search_entry.get().strip()
        if query:
            filtered = self.controller.search_orders(query)
            self.update_data_source(filtered)
            self.show_filter_tag(f"Tìm kiếm: '{query}'")
        else:
            messagebox.showwarning("Thông báo", "Vui lòng nhập nội dung tìm kiếm!")
            self.clear_filter()

    def show_filter_tag(self, text):
        if self.filter_label: self.filter_label.destroy()
        self.filter_label = tk.Frame(self.filter_frame, bg="#d0f0d0")
        self.filter_label.pack(side=tk.LEFT, padx=5)
        tk.Label(self.filter_label, text=text, bg="#d0f0d0").pack(side=tk.LEFT, padx=(5, 2))
        tk.Button(self.filter_label, text="✕", bg="#d0f0d0", bd=0, command=self.clear_filter).pack(side=tk.LEFT)

    def clear_filter(self):
        if self.filter_label: self.filter_label.destroy(); self.filter_label = None
        self.search_entry.delete(0, tk.END)
        self.load_data()

    def on_order_double_click(self, event):
        selection = self.tree.selection()
        if not selection: return
        order_id = self.tree.item(selection[0])["values"][2]
        full_details = self.controller.get_order_details(order_id)
        if full_details:
            self.show_order_popup(full_details)
        else:
            messagebox.showerror("Lỗi", f"Không tìm thấy dữ liệu đơn hàng {order_id}")

    def show_order_popup(self, data):
        order_info = data['order_info']
        cust_name = data['customer_name']
        details = data['products']
        staff_name = data.get('staff_name', f"Mã {order_info.user_id}")
        detail_window = tk.Toplevel(self.master)
        detail_window.title(f"Chi tiết Đơn Hàng {order_info.order_id}")
        detail_window.geometry("700x500")
        detail_window.configure(bg="#f5f5f5")

        main_frame = tk.Frame(detail_window, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        title_frame = tk.Frame(main_frame, bg="#f5f5f5")
        title_frame.pack(fill="x")
        tk.Label(title_frame, text=f"🧾 ĐƠN HÀNG #{order_info.order_id}",
                 font=("Arial", 14, "bold"), bg="#f5f5f5").pack(anchor="w")
        ttk.Separator(title_frame, orient="horizontal").pack(fill="x", pady=(5, 10))

        info_frame = tk.Frame(main_frame, bg="#f5f5f5")
        info_frame.pack(fill="x", pady=(0, 10))
        info_frame.grid_columnconfigure(1, weight=1)
        bold_font = ("Arial", 10, "bold")

        def add_row(r, label, value, fg="black", ft=None):
            tk.Label(info_frame, text=label, font=bold_font, bg="#f5f5f5").grid(row=r, column=0, sticky="w", padx=5,
                                                                                pady=2)
            tk.Label(info_frame, text=value, fg=fg, font=ft, bg="#f5f5f5").grid(row=r, column=1, sticky="w", padx=5,
                                                                                pady=2)

        add_row(0, "Khách hàng:", cust_name)
        add_row(1, "Ngày đặt:", order_info.date)
        add_row(2, "Nhân viên:", staff_name)
        total_val = sum(d.total_price for d in details)
        add_row(3, "Tổng cộng:", f"{total_val:,.0f} VNĐ", fg="#d32f2f", ft=("Arial", 11, "bold"))
        tk.Label(main_frame, text="Chi Tiết Sản Phẩm:", font=bold_font, bg="#f5f5f5").pack(anchor="w", pady=(10, 0))

        tree_container = tk.Frame(main_frame, bd=1, relief="solid")
        tree_container.pack(fill="both", expand=True, pady=5)

        cols = ("Mã SP", "Tên SP", "SL", "Đơn Giá", "Thành Tiền")
        tv = ttk.Treeview(tree_container, columns=cols, show="headings", height=8)
        tv.heading("Mã SP", text="Mã SP");
        tv.column("Mã SP", width=60, anchor="center")
        tv.heading("Tên SP", text="Tên SP");
        tv.column("Tên SP", width=200)
        tv.heading("SL", text="SL");
        tv.column("SL", width=50, anchor="center")
        tv.heading("Đơn Giá", text="Đơn Giá");
        tv.column("Đơn Giá", width=100, anchor="e")
        tv.heading("Thành Tiền", text="Thành Tiền");
        tv.column("Thành Tiền", width=100, anchor="e")

        sc = ttk.Scrollbar(tree_container, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sc.set)
        sc.pack(side="right", fill="y")
        tv.pack(side="left", fill="both", expand=True)

        for d in details:
            tv.insert("", "end", values=(
                d.product.product_id, d.product.product_name, d.quantity,
                f"{d.product.price:,.0f}", f"{d.total_price:,.0f}"
            ))

        ttk.Button(main_frame, text="Đóng", command=detail_window.destroy).pack(side="right", pady=10)

    def create_invoice(self):
        try:
            user_id = self.master.master.current_user_id
        except AttributeError:
            user_id = 1
        AddOrderView(self.master, current_user_id=user_id, callback_success=self.load_data)

    def show_menu_popup(self):
        menu = tk.Menu(self, tearoff=0, font=("Arial", 10))
        menu.add_command(label="Thông báo",
                         command=lambda: handle_check_inventory(self))
        menu.add_separator()
        if self.role == "admin":
            menu.add_command(label="Quản lý tài khoản",
                             command=lambda: handle_open_account(self.main_controller))
            menu.add_separator()
        menu.add_command(label="Đăng xuất",
                         command=lambda: handle_logout(self))
        try:
            x = self.btn_menu.winfo_rootx()
            y = self.btn_menu.winfo_rooty() + self.btn_menu.winfo_height()
            menu.post(x, y)
        except:
            menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'),
                        background=self.BG_CARD, foreground=self.TEXT_SECONDARY, relief="flat")
        style.map("Custom.Treeview.Heading", background=[('active', self.BG_CARD)])
        style.configure("Custom.Treeview", rowheight=30, font=('Arial', 10),
                        background=self.BG_CARD, fieldbackground=self.BG_CARD, relief="flat")
        style.layout("Custom.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])