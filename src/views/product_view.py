import tkinter as tk
from tkinter import ttk, messagebox

from src.controllers.brand_controller import BrandController
from src.controllers.category_controller import CategoryController
from src.controllers.product_controller import ProductController
from src.views.add_product_view import AddProductWindow
from src.utils.menu_helper import handle_open_account, handle_logout, handle_check_inventory
from src.views.brand_view import BrandView
from src.views.category_view import CategoryView
from src.views.product_detail_view import ProductDetailsWindow
import math


class ProductView(tk.Frame):
    def __init__(self, master=None, role=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.role = role if role else 'user'
        self.main_controller = None
        self.pack(fill=tk.BOTH, expand=True)

        self.controller = ProductController()
        self.controller.set_view(self)

        self.category_controller = CategoryController()
        self.brand_controller = BrandController()

        self.listbox_var = tk.StringVar(master=self, value="category")
        self.filter_label = None
        self.current_data = []
        self.current_page = 1
        self.items_per_page = 20
        self.total_pages = 1

        self.BG_CARD = "#ffffff"
        self.TEXT_SECONDARY = "#666666"
        self.setup_styles()

        self.create_widgets()
        self.update_listbox()
        self.show_all_products()
        self.master.bind_all("<Button-1>", self.on_click_anywhere, add="+")

    def create_widgets(self):
        self.header_font = ("Arial", 14, "bold")

        header_frame = tk.Frame(self, height=50, bg="#4CAF50")
        header_frame.pack(side=tk.TOP, fill=tk.X)
        tk.Label(header_frame, text="LOGO", bg="#4CAF50", fg="white",
                 font=self.header_font).pack(side=tk.LEFT, padx=15)
        self.btn_menu = tk.Button(header_frame, text="☰", bg="#4CAF50", fg="white", bd=0,
                                  font=("Arial", 12, "bold"), activebackground="#45a049",
                                  command=self.show_menu_popup)
        self.btn_menu.pack(side=tk.RIGHT, padx=15)
        menu_frame = tk.Frame(self, height=40, bg="#e0e0e0")
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        menu_items = ["Sản phẩm", "Bảo hành", "Đơn hàng", "Khách hàng", "Thống kê"]

        for item in menu_items:
            btn_bg = "#c0c0c0" if item == "Sản phẩm" else "#e0e0e0"

            btn = tk.Button(menu_frame, text=item, bg=btn_bg, fg="#333", bd=0,
                            padx=15, pady=5, activebackground="#d0d0d0")
            btn.pack(side=tk.LEFT, padx=5)
            def on_click(view_name=item):
                if hasattr(self, 'main_controller') and self.main_controller:
                    self.main_controller.switch_view(view_name)
                else:
                    print("Lỗi: Không tìm thấy MainView controller")

            btn.config(command=on_click)

        footer_frame = tk.Frame(self, bg="#005aae")
        footer_frame.pack(side="bottom", fill="x")
        tk.Label(footer_frame, text="Design by Nhóm 14!", fg="white", bg="#005aae",
                 font=("Arial", 14, "bold")).pack(side="left", padx=20, pady=10)

        main_frame = tk.Frame(self, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(2, weight=1)

        sidebar_frame = tk.Frame(main_frame, width=220, bg="white")
        sidebar_frame.grid(row=1, column=0, rowspan=3, sticky="ns", padx=(0, 10))
        sidebar_frame.grid_propagate(False)

        switch_frame = tk.Frame(sidebar_frame, bg="white")
        switch_frame.pack(pady=10)

        self.btn_category = tk.Button(switch_frame, text="Danh mục", width=10,
                                      bg="#4CAF50", fg="white", bd=0,
                                      command=self.show_category)
        self.btn_category.pack(side=tk.LEFT, padx=5)

        self.btn_brand = tk.Button(switch_frame, text="Thương hiệu", width=10,
                                   bg="#f0f0f0", fg="#333", bd=0,
                                   command=self.show_brand)
        self.btn_brand.pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(sidebar_frame, bg="#f9f9f9", bd=0,
                                  highlightthickness=0, relief=tk.FLAT)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        self.listbox.bind("<Button-3>", self.on_right_click_listbox)
        top_frame = tk.Frame(main_frame, bg="#f9f9f9", height=55)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        top_frame.grid_columnconfigure(1, weight=1)

        tk.Label(top_frame, text="Sản phẩm", bg="#f9f9f9",
                 font=self.header_font).grid(row=0, column=0, sticky="w", padx=15, pady=10)

        self.search_entry = tk.Entry(top_frame, bd=0, highlightthickness=1,
                                     highlightbackground="#ccc", relief=tk.FLAT, width=30)
        self.search_entry.grid(row=0, column=1, sticky="e", padx=5)
        self.search_entry.bind("<Return>", self.on_search_enter)

        self.search_button = tk.Button(top_frame, text="Tìm", bg="#4CAF50", fg="white", bd=0,
                                       padx=12, pady=5, relief=tk.FLAT,
                                       activebackground="#45a049",
                                       command=self.on_search_button_click)
        self.search_button.grid(row=0, column=2, sticky="e")

        if self.role == "admin":
            self.add_button = tk.Button(top_frame, text="Thêm", bg="#2196F3", fg="white",
                                        padx=12, pady=5, bd=0, activebackground="#1976D2",
                                        command=self.show_add_menu)
            self.add_button.grid(row=0, column=3, padx=10)
        self.filter_frame = tk.Frame(main_frame, bg="#f0f0f0")
        self.filter_frame.grid(row=1, column=1, sticky="w", pady=(0, 8))
        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.grid(row=2, column=1, sticky="nsew")

        columns = ("#", "Tên SP", "Số lượng", "Giá bán", "Thời gian BH", "Thương hiệu", "Danh mục")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Custom.Treeview")
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background=self.BG_CARD)

        self.tree.heading("#", text="#")
        self.tree.column("#", width=50, anchor=tk.CENTER)
        self.tree.heading("Tên SP", text="Tên SP")
        self.tree.column("Tên SP", width=200, anchor=tk.W)
        self.tree.heading("Số lượng", text="Số lượng")
        self.tree.column("Số lượng", width=80, anchor=tk.CENTER)
        self.tree.heading("Giá bán", text="Giá bán")
        self.tree.column("Giá bán", width=120, anchor=tk.E)
        self.tree.heading("Thời gian BH", text="Bảo hành")
        self.tree.column("Thời gian BH", width=100, anchor=tk.CENTER)
        self.tree.heading("Thương hiệu", text="Thương hiệu")
        self.tree.column("Thương hiệu", width=120, anchor=tk.W)
        self.tree.heading("Danh mục", text="Danh mục")
        self.tree.column("Danh mục", width=120, anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<Double-1>", self.on_treeview_double_click)
        pagination_frame = tk.Frame(main_frame, bg="#f0f0f0")
        pagination_frame.grid(row=3, column=1, sticky="ew", pady=5)
        self.btn_next = tk.Button(pagination_frame, text=">", command=self.next_page,
                                  bd=0, highlightthickness=0, relief=tk.FLAT)
        self.btn_next.pack(side=tk.RIGHT, padx=5)

        self.lbl_page_info = tk.Label(pagination_frame, text="Trang 1 / 1", bg="#f0f0f0", font=("Arial", 10))
        self.lbl_page_info.pack(side=tk.RIGHT, padx=10)

        self.btn_prev = tk.Button(pagination_frame, text="<", command=self.prev_page,
                                  bd=0, highlightthickness=0, relief=tk.FLAT)
        self.btn_prev.pack(side=tk.RIGHT, padx=5)

    def render_treeview(self):
        self.tree.delete(*self.tree.get_children())
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page
        page_items = self.current_data[start_index:end_index]
        for i, item in enumerate(page_items):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", tk.END, values=item, tags=(tag,))

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
        if self.current_page > 1:
            self.current_page -= 1
            self.render_treeview()

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.render_treeview()

    def show_all_products(self):
        product_list = self.controller.get_all_products_for_view()
        self.update_data_source(product_list)

    def on_listbox_select(self, event):
        sel = self.listbox.curselection()
        if not sel: return
        selected_name = self.listbox.get(sel[0])

        if self.listbox_var.get() == "category":
            filtered = self.controller.filter_by_category_for_view(selected_name)
            self.show_filter_label(f"Danh mục: {selected_name}")
        else:
            filtered = self.controller.filter_by_brand_for_view(selected_name)
            self.show_filter_label(f"Thương hiệu: {selected_name}")

        self.update_data_source(filtered)
        self.search_entry.delete(0, tk.END)

    def perform_search(self):
        q = self.search_entry.get().strip().lower()
        if not q:
            messagebox.showwarning("Thông báo", "Vui lòng nhập nội dung tìm kiếm!")
            return
        filtered = self.controller.search_products_for_view(q)
        self.update_data_source(filtered)
        self.show_filter_label(f"Tìm kiếm: '{q}'")
        self.listbox.selection_clear(0, tk.END)

    def refresh_data(self):
        self.clear_filter()

    def show_filter_label(self, text):
        if self.filter_label: self.filter_label.destroy()
        self.filter_label = tk.Frame(self.filter_frame, bg="#d0f0d0")
        self.filter_label.pack(side=tk.LEFT, padx=5)
        tk.Label(self.filter_label, text=text, bg="#d0f0d0", fg="#333").pack(side=tk.LEFT, padx=(5, 2))
        tk.Button(self.filter_label, text="✕", bg="#d0f0d0", bd=0, command=self.clear_filter).pack(side=tk.LEFT)

    def clear_filter(self):
        if self.filter_label: self.filter_label.destroy()
        self.filter_label = None
        self.show_all_products()
        self.listbox.selection_clear(0, tk.END)

    def show_add_menu(self):
        menu = tk.Menu(self.master, tearoff=0)
        menu.add_command(label="Thêm sản phẩm", command=self.add_product_window)
        menu.add_separator()
        menu.add_command(label="Thêm danh mục", command=self.add_category_window)
        menu.add_separator()
        menu.add_command(label="Thêm thương hiệu", command=self.add_brand_window)
        x = self.add_button.winfo_rootx()
        y = self.add_button.winfo_rooty() + self.add_button.winfo_height()
        menu.post(x, y)

    def add_product_window(self):
        AddProductWindow(self.master, self.controller)

    def add_category_window(self):
        win = tk.Toplevel(self.master)
        win.title("Thêm danh mục")
        win.geometry("400x250")
        win.resizable(False, False)
        win.configure(bg="#f5f5f5")
        main_frame = tk.Frame(win, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=1)
        tk.Label(main_frame, text="Tên danh mục:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=0, column=0,
                                                                                                  sticky="w", pady=5)
        entry_ten = tk.Entry(main_frame, width=40)
        entry_ten.grid(row=0, column=1, sticky="we", pady=5, padx=5)
        tk.Label(main_frame, text="Mô tả:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="nw",
                                                                                           pady=5)
        text_mo_ta = tk.Text(main_frame, height=5, width=40, relief="solid", bd=1)
        text_mo_ta.grid(row=1, column=1, sticky="we", pady=5, padx=5)
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=10)
        save_cmd = lambda: self.on_save_category(win, entry_ten, text_mo_ta)
        tk.Button(btn_frame, text="Lưu", bg="#4CAF50", fg="white", padx=15, pady=5, relief="flat",
                  command=save_cmd).pack(side="left")
        tk.Button(btn_frame, text="Hủy", bg="#f44336", fg="white", padx=15, pady=5, relief="flat",
                  command=win.destroy).pack(side="left", padx=10)

    def on_save_category(self, win, entry_ten, text_mo_ta):
        ten = entry_ten.get().strip()
        mo_ta = text_mo_ta.get("1.0", "end-1c").strip()
        if not ten:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tên danh mục.", parent=win)
            return
        success, msg = self.controller.handle_add_category(ten, mo_ta)
        if success:
            messagebox.showinfo("Thông báo", msg, parent=win)
            win.destroy()
        else:
            messagebox.showerror("Lỗi", msg, parent=win)

    def add_brand_window(self):
        win = tk.Toplevel(self.master)
        win.title("Thêm thương hiệu")
        win.geometry("400x300")
        win.resizable(False, False)
        win.configure(bg="#f5f5f5")
        main_frame = tk.Frame(win, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        main_frame.grid_columnconfigure(1, weight=1)
        tk.Label(main_frame, text="Tên thương hiệu:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=0, column=0,
                                                                                                     sticky="w", pady=5)
        entry_ten = tk.Entry(main_frame, width=40)
        entry_ten.grid(row=0, column=1, sticky="we", pady=5, padx=5)
        tk.Label(main_frame, text="Mô tả:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="nw",
                                                                                           pady=5)
        text_mo_ta = tk.Text(main_frame, height=5, width=40, relief="solid", bd=1)
        text_mo_ta.grid(row=1, column=1, sticky="we", pady=5, padx=5)
        tk.Label(main_frame, text="Quốc gia:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=2, column=0,
                                                                                              sticky="w", pady=5)
        entry_quoc_gia = tk.Entry(main_frame, width=40)
        entry_quoc_gia.grid(row=2, column=1, sticky="we", pady=5, padx=5)
        btn_frame = tk.Frame(main_frame, bg="#f5f5f5")
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=10)
        save_cmd = lambda: self.on_save_brand(win, entry_ten, text_mo_ta, entry_quoc_gia)
        tk.Button(btn_frame, text="Lưu", bg="#4CAF50", fg="white", padx=15, pady=5, relief="flat",
                  command=save_cmd).pack(side="left")
        tk.Button(btn_frame, text="Hủy", bg="#f44336", fg="white", padx=15, pady=5, relief="flat",
                  command=win.destroy).pack(side="left", padx=10)

    def on_save_brand(self, win, entry_ten, text_mo_ta, entry_quoc_gia):
        ten = entry_ten.get().strip()
        mo_ta = text_mo_ta.get("1.0", "end-1c").strip()
        quoc_gia = entry_quoc_gia.get().strip()
        if not ten:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tên thương hiệu.", parent=win)
            return
        success, msg = self.controller.handle_add_brand(ten, mo_ta, quoc_gia)
        if success:
            messagebox.showinfo("Thông báo", msg, parent=win)
            win.destroy()
        else:
            messagebox.showerror("Lỗi", msg, parent=win)

    def on_treeview_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item: return
        values_from_tree = self.tree.item(selected_item[0])["values"]
        product_id = int(values_from_tree[0])
        full_product_data = self.controller.get_full_product(product_id)
        if not full_product_data:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu đầy đủ cho sản phẩm.")
            return
        ProductDetailsWindow(self.master, full_product_data, self.controller, role=self.role)

    def show_category(self):
        self.listbox_var.set("category")
        self.update_listbox()
        self.btn_category.config(bg="#4CAF50", fg="white")
        self.btn_brand.config(bg="#f0f0f0", fg="#333")

    def show_brand(self):
        self.listbox_var.set("brand")
        self.update_listbox()
        self.btn_brand.config(bg="#4CAF50", fg="white")
        self.btn_category.config(bg="#f0f0f0", fg="#333")

    # def update_listbox(self):
    #     self.listbox.delete(0, tk.END)
    #     if self.listbox_var.get() == "category":
    #         data = self.controller.get_category_names()
    #     else:
    #         data = self.controller.get_brand_names()
    #     for item in data:
    #         self.listbox.insert(tk.END, item)

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        current_mode = self.listbox_var.get()
        if current_mode == "category":
            categories = self.category_controller.get_all_categories()
            data = [cat.category_name for cat in categories]
        else:
            brands = self.brand_controller.get_all_brands()
            data = [brand.brand_name for brand in brands]

        for item in data:
            self.listbox.insert(tk.END, item)

    def on_search_enter(self, event):
        self.perform_search()

    def on_search_button_click(self):
        self.perform_search()

    def on_click_anywhere(self, event):
        try:
            if not self.listbox.winfo_exists() or not self.tree.winfo_exists():
                return
        except Exception:
            return
        widget = event.widget
        if not str(widget).startswith(str(self.listbox)):
            self.listbox.selection_clear(0, tk.END)
        if not str(widget).startswith(str(self.tree)):
            self.tree.selection_remove(*self.tree.selection())

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

    def on_right_click_listbox(self, event):
        try:
            index = self.listbox.nearest(event.y)
            if index == -1:
                return
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Xem chi tiết", command=lambda: self.handle_detail_popup(index))
            menu.post(event.x_root, event.y_root)
        except Exception as e:
            print(f"Error on right click: {e}")

    def handle_detail_popup(self, index):
        selected_name = self.listbox.get(index)
        mode = self.listbox_var.get()
        if mode == "category":
            self.open_category_detail(selected_name)
        else:
            self.open_brand_detail(selected_name)

    def open_category_detail(self, name):
        all_cats = self.category_controller.get_all_categories()
        target_cat = next((c for c in all_cats if c.category_name == name), None)

        if target_cat:
            CategoryView(
                self.master,
                category=target_cat,
                controller=self.category_controller,
                role=self.role,
                refresh_callback=self.refresh_listbox_data
            )
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu danh mục này.")

    def open_brand_detail(self, name):
        all_brands = self.brand_controller.get_all_brands()
        target_brand = next((b for b in all_brands if b.brand_name == name), None)

        if target_brand:
            BrandView(
                self.master,
                brand=target_brand,
                controller=self.brand_controller,
                role=self.role,
                refresh_callback=self.refresh_listbox_data
            )
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy dữ liệu thương hiệu này.")

    def refresh_listbox_data(self):
        self.update_listbox()
        self.listbox.selection_clear(0, tk.END)
        self.clear_filter()
        self.refresh_data()