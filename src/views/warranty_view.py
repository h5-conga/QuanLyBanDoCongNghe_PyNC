import tkinter as tk
from tkinter import ttk, messagebox
import math
from src.controllers.warranty_controller import WarrantyController
from src.utils.menu_helper import handle_logout, handle_open_account, handle_check_inventory


class WarrantyView(tk.Frame):
    def __init__(self, master=None, role=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.role = role if role else 'user'
        self.controller = WarrantyController()
        self.main_controller = None
        self.pack(fill=tk.BOTH, expand=True)
        self.header_font = ("Arial", 14, "bold")
        self.filter_label = None
        self.current_filter_status = "all"
        self.current_data = []
        self.current_page = 1
        self.items_per_page = 20
        self.total_pages = 1

        self.BG_CARD = "#ffffff"
        self.TEXT_SECONDARY = "#666666"
        self.setup_styles()

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        header_frame = tk.Frame(self, height=50, bg="#4CAF50")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header_frame, text="LOGO", bg="#4CAF50", fg="white",
                 font=self.header_font).pack(side=tk.LEFT, padx=15)
        self.btn_menu = tk.Button(header_frame, text="☰", bg="#4CAF50", fg="white", bd=0,
                                  font=("Arial", 12, "bold"), activebackground="#45a049",
                                  command=self.show_menu_popup)  # Gọi hàm hiển thị
        self.btn_menu.pack(side=tk.RIGHT, padx=15)
        menu_frame = tk.Frame(self, height=40, bg="#e0e0e0")
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        menu_items = ["Sản phẩm", "Bảo hành", "Đơn hàng", "Khách hàng", "Thống kê"]

        for item in menu_items:
            btn_bg = "#c0c0c0" if item == "Bảo hành" else "#e0e0e0"  # Tô đậm nút Bảo hành

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
        top_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        top_frame.grid_columnconfigure(1, weight=1)

        tk.Label(top_frame, text="Bảo hành", bg="#f9f9f9",
                 font=self.header_font).grid(row=0, column=0, sticky="w", padx=15)
        self.search_entry = tk.Entry(top_frame, bd=0, highlightthickness=1,
                                     highlightbackground="#ccc", relief=tk.FLAT, width=30)
        self.search_entry.grid(row=0, column=2, sticky="e", padx=(5, 5))
        self.search_entry.bind("<Return>", self.on_search_enter)
        self.search_button = tk.Button(top_frame, text="Tìm", bg="#4CAF50", fg="white", bd=0,
                                       padx=12, pady=5, relief=tk.FLAT, activebackground="#45a049",
                                       command=self.on_search_button_click)
        self.search_button.grid(row=0, column=3, sticky="e", padx=(0, 10))
        self.filter_combobox = ttk.Combobox(top_frame, state="readonly", width=15)
        self.filter_combobox['values'] = ["Tất cả", "Còn hạn", "Đã hết hạn"]
        self.filter_combobox.current(0)  # Chọn mặc định "Tất cả"
        self.filter_combobox.grid(row=0, column=4, sticky="e", padx=(0, 15))
        self.filter_combobox.bind("<<ComboboxSelected>>", self.on_filter_change)

        self.filter_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.grid(row=2, column=0, sticky="nsew")
        columns = ("#ID", "Khách hàng", "Mã SP", "Tên SP", "Điện thoại", "Ngày bắt đầu", "Thời gian (tháng)",
                   "Ngày kết thúc")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Custom.Treeview")
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background=self.BG_CARD)

        for col in columns:
            self.tree.heading(col, text=col)
            if col in ["#ID", "Mã SP", "Thời gian (tháng)"]:
                self.tree.column(col, width=80, anchor=tk.CENTER)
            elif col in ["Ngày bắt đầu", "Ngày kết thúc", "Điện thoại"]:
                self.tree.column(col, width=120, anchor=tk.CENTER)
            else:
                self.tree.column(col, width=150, anchor=tk.W)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        pagination_frame = tk.Frame(main_frame, bg="#f0f0f0")
        pagination_frame.grid(row=3, column=0, sticky="ew", pady=5)
        self.btn_next = tk.Button(pagination_frame, text=">", command=self.next_page,
                                  bd=0, relief="solid")
        self.btn_next.pack(side=tk.RIGHT, padx=5)
        self.lbl_page_info = tk.Label(pagination_frame, text="Trang 1 / 1", bg="#f0f0f0", font=("Arial", 10))
        self.lbl_page_info.pack(side=tk.RIGHT, padx=10)
        self.btn_prev = tk.Button(pagination_frame, text="<", command=self.prev_page,
                                  bd=0, relief="solid")
        self.btn_prev.pack(side=tk.RIGHT, padx=5)

    def render_treeview(self):
        self.tree.delete(*self.tree.get_children())
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_items = self.current_data[start_index:end_index]
        for i, row in enumerate(page_items):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=row, tags=(tag,))

        self.total_pages = math.ceil(len(self.current_data) / self.items_per_page)
        if self.total_pages == 0: self.total_pages = 1
        self.lbl_page_info.config(text=f"Trang {self.current_page} / {self.total_pages}")
        self.btn_prev.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.btn_next.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)

    def update_data_source(self, new_data):
        self.current_data = new_data
        self.current_page = 1
        self.render_treeview()

        if new_data:
            try:
                new_data.sort(key=lambda x: int(x[0]) if str(x[0]).isdigit() else x[0], reverse=False)
            except Exception:
                pass
        self.current_data = new_data
        self.current_page = 1
        self.render_treeview()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.render_treeview()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.render_treeview()

    def on_filter_change(self):
        selection = self.filter_combobox.get()
        status_map = {
            "Tất cả": "all",
            "Còn hạn": "active",
            "Đã hết hạn": "expired"
        }
        status_key = status_map.get(selection, "all")
        data = self.controller.filter_by_status(status_key)
        self.update_data_source(data)
        self.search_entry.delete(0, tk.END)
        if self.filter_label:
            self.filter_label.destroy()
            self.filter_label = None
    def load_data(self):
        self.filter_combobox.set("Tất cả")  # Reset combobox
        data = self.controller.get_all_warranties_for_view()
        self.update_data_source(data)

    def on_search_enter(self, event):
        self.perform_search()

    def on_search_button_click(self):
        self.perform_search()

    def perform_search(self):
        query = self.search_entry.get().strip()
        if query:
            self.filter_combobox.set("Tất cả")

            filtered_data = self.controller.search_warranties(query)
            self.update_data_source(filtered_data)
            self.show_filter_tag(f"Tìm kiếm: '{query}'")
        else:
            messagebox.showwarning("Thông báo", "Vui lòng nhập nội dung tìm kiếm!")
            self.clear_filter()

    def show_filter_tag(self, text):
        if self.filter_label:
            self.filter_label.destroy()
        self.filter_label = tk.Frame(self.filter_frame, bg="#d0f0d0")
        self.filter_label.pack(side=tk.LEFT, padx=15)
        tk.Label(self.filter_label, text=text, bg="#d0f0d0").pack(side=tk.LEFT, padx=(5, 2))
        tk.Button(self.filter_label, text="✕", bg="#d0f0d0", bd=0,
                  command=self.clear_filter).pack(side=tk.LEFT)

    def clear_filter(self):
        if self.filter_label:
            self.filter_label.destroy()
            self.filter_label = None
        self.search_entry.delete(0, tk.END)
        self.load_data()

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