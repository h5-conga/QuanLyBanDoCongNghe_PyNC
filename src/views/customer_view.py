import tkinter as tk
from tkinter import ttk
from src.controllers.customer_controller import CustomerController
from src.views.add_customer_view import AddCustomerView
from src.utils.menu_helper import handle_logout, handle_open_account, handle_check_inventory


class CustomerView(tk.Frame):
    def __init__(self, master=None, role=None):
        super().__init__(master)
        self.main_controller = None
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.role= None if role else "user"
        self.BG_MAIN = "#f0f0f0"
        self.BG_CARD = "#ffffff"
        self.TEXT_PRIMARY = "#222222"
        self.TEXT_SECONDARY = "#666666"

        self.config(bg=self.BG_MAIN)
        self.header_font = ("Arial", 14, "bold")
        self.controller = CustomerController()
        self.controller.set_view(self)
        self.items_per_page = 25
        self.current_page = 1
        self.total_pages = 1
        self.all_customer_data = []
        self.setup_styles()
        self.create_widgets()
        self.refresh_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview.Heading", font=('Arial', 10, 'bold'),
                        background=self.BG_CARD, foreground=self.TEXT_SECONDARY, relief="flat")
        style.map("Custom.Treeview.Heading", background=[('active', self.BG_CARD)])
        style.configure("Custom.Treeview", rowheight=30, font=('Arial', 10),
                        background=self.BG_CARD, fieldbackground=self.BG_CARD, relief="flat")
        style.layout("Custom.Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        style.configure("TCombobox", font=('Arial', 10), padding=5)
        style.map("TCombobox", fieldbackground=[('readonly', '#ffffff')], foreground=[('readonly', '#333333')])

    def on_search_focus_in(self, event):
        if self.entry_search.get() == self.placeholder_text:
            self.entry_search.delete(0, tk.END)
            self.entry_search.config(fg=self.TEXT_PRIMARY)

    def on_search_focus_out(self, event):
        if self.entry_search.get() == "":
            self.entry_search.insert(0, self.placeholder_text)
            self.entry_search.config(fg=self.TEXT_SECONDARY)

    def create_widgets(self):
        header_frame = tk.Frame(self, height=50, bg="#4CAF50")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header_frame, text="LOGO", bg="#4CAF50", fg="white", font=self.header_font).pack(side=tk.LEFT, padx=15)
        self.btn_menu = tk.Button(header_frame, text="☰", bg="#4CAF50", fg="white", bd=0,
                                  font=("Arial", 12, "bold"), activebackground="#45a049",
                                  command=self.show_menu_popup)  # Gọi hàm hiển thị
        self.btn_menu.pack(side=tk.RIGHT, padx=15)

        menu_frame = tk.Frame(self, height=40, bg="#e0e0e0")
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        menu_items = ["Sản phẩm", "Bảo hành", "Đơn hàng", "Khách hàng", "Thống kê"]

        for item in menu_items:
            btn_bg = "#c0c0c0" if item == "Khách hàng" else "#e0e0e0"  # Tô đậm nút Đơn hàng
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

        main_content = tk.Frame(self, bg=self.BG_MAIN)
        main_content.pack(fill=tk.BOTH, expand=True)
        right_area_frame = tk.Frame(main_content, bg=self.BG_MAIN)
        right_area_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        header_bar = tk.Frame(right_area_frame, bg="#f0f0f0", height=60)
        header_bar.pack(side=tk.TOP, fill=tk.X, pady=(0, 1))
        header_bar.pack_propagate(False)

        tk.Label(header_bar, text="Khách hàng", font=('Arial', 16, 'bold'),
                 bg="#f0f0f0", fg=self.TEXT_PRIMARY).pack(side=tk.LEFT, padx=20)

        search_frame = tk.Frame(header_bar, bg=self.BG_CARD)
        search_frame.pack(side=tk.LEFT, padx=30, pady=10)

        self.entry_search = tk.Entry(search_frame, font=('Arial', 11), width=40, relief=tk.FLAT,
                                     bg=self.BG_CARD, fg=self.TEXT_SECONDARY)
        self.placeholder_text = "Tìm kiếm theo tên, điện thoại..."
        self.entry_search.insert(0, self.placeholder_text)
        self.entry_search.bind("<FocusIn>", self.on_search_focus_in)
        self.entry_search.bind("<FocusOut>", self.on_search_focus_out)
        self.entry_search.bind("<Return>", lambda event: self.perform_search())
        self.entry_search.pack(side=tk.LEFT, padx=(10, 10), ipady=5)

        tk.Button(header_bar, text="Thêm mới", relief=tk.RAISED, bg="#4CAF50", fg="white",
                  font=('Arial', 10, 'bold'), command=self.open_add_customer_window).pack(side=tk.RIGHT, padx=20,
                                                                                          pady=10)

        tk.Button(header_bar, text="Tìm kiếm", relief=tk.RAISED, bg="#007bff", fg="white",
                  font=('Arial', 10, 'bold'), command=self.perform_search).pack(side=tk.RIGHT, padx=(0, 0), pady=10)

        content_frame = tk.Frame(right_area_frame, bg=self.BG_CARD)
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        table_container = tk.Frame(content_frame, bg=self.BG_CARD)
        table_container.pack(fill=tk.BOTH, expand=True)
        self.create_customer_table(table_container)

        pagination_frame = tk.Frame(content_frame, bg=self.BG_CARD)
        pagination_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        self.create_pagination_controls(pagination_frame)

    def create_customer_table(self, parent):
        cols = ("Mã khách hàng", "Tên khách hàng", "Địa chỉ", "Điện thoại", "Email")
        self.customer_tree = ttk.Treeview(parent, columns=cols, show="headings", style="Custom.Treeview")

        self.customer_tree.heading("Mã khách hàng", text="Mã KH", anchor="center")
        self.customer_tree.column("Mã khách hàng", width=80, anchor="center")

        self.customer_tree.heading("Tên khách hàng", text="Tên khách hàng", anchor="w")
        self.customer_tree.column("Tên khách hàng", width=180, anchor="w")

        self.customer_tree.heading("Địa chỉ", text="Địa chỉ", anchor="w")
        self.customer_tree.column("Địa chỉ", width=250, anchor="w")

        self.customer_tree.heading("Điện thoại", text="Điện thoại", anchor="center")
        self.customer_tree.column("Điện thoại", width=100, anchor="center")

        self.customer_tree.heading("Email", text="Email", anchor="w")
        self.customer_tree.column("Email", width=150, anchor="w")

        self.customer_tree.tag_configure("oddrow", background="#f9f9f9")
        self.customer_tree.tag_configure("evenrow", background=self.BG_CARD)
        self.customer_tree.pack(fill=tk.BOTH, expand=True)

    def create_pagination_controls(self, parent):
        button_frame = tk.Frame(parent, bg=self.BG_CARD)
        button_frame.pack(side=tk.RIGHT, padx=10)
        self.btn_prev_page = tk.Button(button_frame, text="<", command=self.go_prev_page, relief=tk.FLAT,
                                       bg=self.BG_CARD)
        self.btn_prev_page.pack(side=tk.LEFT, padx=2)
        self.lbl_page_status = tk.Label(button_frame, text="Trang 1 / 1", font=("Arial", 10), bg=self.BG_CARD)
        self.lbl_page_status.pack(side=tk.LEFT, padx=5)
        self.btn_next_page = tk.Button(button_frame, text=">", command=self.go_next_page, relief=tk.FLAT,
                                       bg=self.BG_CARD)
        self.btn_next_page.pack(side=tk.LEFT, padx=2)
    def refresh_data(self):
        self.all_customer_data = self.controller.get_all_customers_for_view()
        total_items = len(self.all_customer_data)
        if total_items == 0:
            self.total_pages = 1
        else:
            self.total_pages = (total_items + self.items_per_page - 1) // self.items_per_page
        self.current_page = 1
        self.load_page_data()

    def load_page_data(self):
        self.customer_tree.delete(*self.customer_tree.get_children())
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = self.current_page * self.items_per_page
        page_data = self.all_customer_data[start_index:end_index]

        for i, row_data in enumerate(page_data):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.customer_tree.insert("", "end", values=row_data, tags=(tag,))

        self.lbl_page_status.config(text=f"Trang {self.current_page} / {self.total_pages}")
        self.btn_prev_page.config(state="normal" if self.current_page > 1 else "disabled")
        self.btn_next_page.config(state="normal" if self.current_page < self.total_pages else "disabled")

    def perform_search(self):
        keyword = self.entry_search.get().strip()
        if not keyword or keyword == self.placeholder_text:
            self.refresh_data()
            return
        self.all_customer_data = self.controller.search_customers(keyword)
        self.current_page = 1
        self.total_pages = max(1, (len(self.all_customer_data) + self.items_per_page - 1) // self.items_per_page)
        self.load_page_data()

    def go_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page_data()

    def go_next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.load_page_data()

    def open_add_customer_window(self):
        AddCustomerView(self, self.controller, self.refresh_data)

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
