import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.controllers.statistics_controller import StatisticsController
from src.utils.menu_helper import handle_logout, handle_open_account, handle_check_inventory


class StatisticsView(tk.Frame):
    def __init__(self, master=None, role=None):
        super().__init__(master, bg="#f0f0f0")
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.role = role if role else 'user'
        self.main_controller = None
        self.controller = StatisticsController()
        self.current_canvas = None
        self.header_font = ("Arial", 14, "bold")
        self.create_widgets()
        self.filter_label = None
        self.show_stats_revenue_month()

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
            btn_bg = "#c0c0c0" if item == "Thống kê" else "#e0e0e0"  # Tô đậm nút Đơn hàng
            btn = tk.Button(menu_frame, text=item, bg=btn_bg, fg="#333", bd=0,
                            padx=15, pady=5, activebackground="#d0d0d0")
            btn.pack(side=tk.LEFT, padx=5)

            def on_click(view_name=item):
                if hasattr(self, 'main_controller') and self.main_controller:
                    self.main_controller.switch_view(view_name)

            btn.config(command=on_click)
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.sidebar_frame = tk.Frame(self.main_frame, width=220, relief=tk.GROOVE, bd=1)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        self.sidebar_frame.pack_propagate(False)

        sidebar_title = ttk.Label(self.sidebar_frame, text="LỰA CHỌN THỐNG KÊ", font=("Arial", 12, "bold"))
        sidebar_title.pack(pady=10)

        revenue_container = tk.Frame(self.sidebar_frame, bg="#ffffff")
        revenue_container.pack(fill=tk.X, padx=10, pady=5)
        title_frame = tk.Frame(revenue_container, bg="#00a0e9", relief=tk.RAISED, borderwidth=2)
        title_frame.pack(fill=tk.X, anchor="n")
        tk.Label(title_frame, text="Doanh thu", bg="#00a0e9", fg="white", font=("Arial", 11, "bold")).pack(fill=tk.X,
                                                                                                           padx=10,
                                                                                                           pady=5)

        self.btn_stats_month = tk.Button(revenue_container, text="Doanh thu theo Tháng",
                                         command=self.show_stats_revenue_month,
                                         bg="#005A9E", fg="#FFFFFF", font=("Arial", 10))
        self.btn_stats_month.pack(fill=tk.X, padx=5, pady=(10, 2))

        self.btn_stats_quarter = tk.Button(revenue_container, text="Doanh thu theo Quý",
                                           command=self.show_stats_revenue_quarter,
                                           bg="#005A9E", fg="#FFFFFF", font=("Arial", 10))
        self.btn_stats_quarter.pack(fill=tk.X, padx=5, pady=(10, 2))

        self.btn_stats_year = tk.Button(revenue_container, text="Doanh thu theo Năm",
                                        command=self.show_stats_revenue_year,
                                        bg="#005A9E", fg="#FFFFFF", font=("Arial", 10))
        self.btn_stats_year.pack(fill=tk.X, padx=5, pady=(10, 2))

        custom_container = tk.Frame(self.sidebar_frame, bg="#ffffff")
        custom_container.pack(fill=tk.X, padx=10, pady=(30, 5))
        title_frame_2 = tk.Frame(custom_container, bg="#00a0e9", relief=tk.RAISED, borderwidth=2)
        title_frame_2.pack(fill=tk.X, anchor="n")
        tk.Label(title_frame_2, text="Doanh thu tùy chỉnh", bg="#00a0e9", fg="white", font=("Arial", 11, "bold")).pack(
            fill=tk.X, padx=10, pady=5)

        tk.Label(custom_container, text="Ngày bắt đầu :", bg="#ffffff", font=("Arial", 10)).pack(fill=tk.X, padx=5,
                                                                                                 pady=(5, 0))
        self.entry_start_date = DateEntry(custom_container, date_pattern='dd/mm/yyyy', width=18)
        self.entry_start_date.pack(fill=tk.X, padx=5, pady=(0, 5))

        tk.Label(custom_container, text="Đến ngày :", bg="#ffffff", font=("Arial", 10)).pack(fill=tk.X, padx=5)
        self.entry_end_date = DateEntry(custom_container, date_pattern='dd/mm/yyyy', width=18)
        self.entry_end_date.pack(fill=tk.X, padx=5, pady=(0, 5))

        self.btn_stats_range = tk.Button(custom_container, text="Xem báo cáo",
                                         command=self.show_stats_custom_range,
                                         bg="#005A9E", fg="#FFFFFF", font=("Arial", 10))
        self.btn_stats_range.pack(fill=tk.X, padx=5, pady=5)

        product_container = tk.Frame(self.sidebar_frame, bg="#ffffff")
        product_container.pack(fill=tk.X, padx=10, pady=(30, 5))
        title_frame_3 = tk.Frame(product_container, bg="#00a0e9", relief=tk.RAISED, borderwidth=2)
        title_frame_3.pack(fill=tk.X, anchor="n")
        tk.Label(title_frame_3, text="Sản phẩm", bg="#00a0e9", fg="white", font=("Arial", 11, "bold")).pack(fill=tk.X,
                                                                                                            padx=10,
                                                                                                            pady=5)

        self.btn_stats_top_products = tk.Button(product_container, text="Top 5 SP theo doanh thu",
                                                command=self.show_stats_top_products,
                                                bg="#005A9E", fg="#FFFFFF", font=("Arial", 10))
        self.btn_stats_top_products.pack(fill=tk.X, padx=5, pady=(10, 2))

        self.btn_stats_top_quantity = tk.Button(product_container,
                                            text="Top 5 SP theo Số lượng",  # <--- SỬA TEXT
                                            command=self.show_stats_products_top_quantity,
                                            bg="#005A9E", fg="#FFFFFF", font=("Arial", 10))
        self.btn_stats_top_quantity.pack(fill=tk.X, padx=5, pady=(10, 2))

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        header_bar = tk.Frame(self.right_frame, bg="#f0f0f0")
        header_bar.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self.title_label = tk.Label(header_bar, text="KẾT QUẢ THỐNG KÊ", font=("Arial", 14, "bold"), bg="#f0f0f0",
                                    fg="#333333")
        self.title_label.pack(side=tk.LEFT, anchor="w", padx=10, pady=5)

        button_frame = tk.Frame(header_bar, bg="#f0f0f0")
        button_frame.pack(side=tk.RIGHT, padx=10)

        # --- Nút 1: Làm mới (Refresh) ---
        self.btn_refresh = tk.Button(button_frame,
                                     text="Làm mới",
                                     bg="#f0ad4e", fg="white",  # Màu cam
                                     font=("Arial", 9, "bold"),
                                     relief=tk.RAISED,
                                     padx=15, pady=3,
                                     activebackground="#ec971f",
                                     activeforeground="white",
                                     command=self.refresh_current_stats)  # Hàm xử lý
        self.btn_refresh.pack(side=tk.LEFT, padx=5)

        self.btn_export = tk.Button(button_frame,
                                    text="Xuất Excel",
                                    bg="#217346", fg="white",  # Màu xanh Excel
                                    font=("Arial", 9, "bold"),
                                    relief=tk.RAISED,
                                    padx=15, pady=3,
                                    activebackground="#1e6b41",
                                    activeforeground="white",
                                    command=self.export_to_excel)  # Hàm xử lý
        self.btn_export.pack(side=tk.LEFT, padx=5)

        self.summary_frame = tk.Frame(self.right_frame, relief=tk.GROOVE, bd=1, bg="#ffffff")
        self.summary_frame.pack(fill=tk.X, pady=5)

        frame_revenue = tk.Frame(self.summary_frame, bg="#ffffff")
        frame_revenue.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)
        tk.Label(frame_revenue, text="Tổng doanh thu", font=("Arial", 10), bg="#ffffff", fg="#555555").pack(side=tk.TOP)
        self.lbl_total_revenue = tk.Label(frame_revenue, text="0 đ", font=("Arial", 12, "bold"), bg="#ffffff",
                                          fg="#005A9E")
        self.lbl_total_revenue.pack(side=tk.TOP)
        frame_orders = tk.Frame(self.summary_frame, bg="#ffffff")
        frame_orders.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)
        tk.Label(frame_orders, text="Tổng đơn hàng", font=("Arial", 10), bg="#ffffff", fg="#555555").pack(side=tk.TOP)
        self.lbl_total_orders = tk.Label(frame_orders, text="0", font=("Arial", 12, "bold"), bg="#ffffff", fg="#00a0e9")
        self.lbl_total_orders.pack(side=tk.TOP)

        frame_product = tk.Frame(self.summary_frame, bg="#ffffff")
        frame_product.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)
        tk.Label(frame_product, text="Sản phẩm bán chạy nhất", font=("Arial", 10), bg="#ffffff", fg="#555555").pack(
            side=tk.TOP)
        self.lbl_top_product = tk.Label(frame_product, text="Chưa có", font=("Arial", 12, "bold"), bg="#ffffff",
                                        fg="#008000")
        self.lbl_top_product.pack(side=tk.TOP)

        self.chart_frame = tk.Frame(self.right_frame, bg="white", bd=1, relief=tk.RIDGE)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        self.result_tree = ttk.Treeview(self.right_frame, height=5)
        self.result_tree.pack(fill=tk.X, pady=5)

        footer_frame = tk.Frame(self.master, bg="#005aae")
        footer_frame.pack(side="bottom", fill="x")
        tk.Label(footer_frame, text="Design by Nhóm 14!", fg="white", bg="#005aae", font=("Arial", 14, "bold")).pack(
            side="left", padx=20, pady=10)


    def draw_chart(self, labels, values, title, xlabel, ylabel, chart_type='bar'):
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()

        fig = plt.Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        colors_bar = ['#4F81BD']  # Xanh dịu
        colors_pie = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']  # Màu Pastel

        if chart_type == 'pie':
            explode = [0.05 if i == 0 else 0 for i in range(len(values))]

            wedges, texts, autotexts = ax.pie(
                values,
                labels=None,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors_pie,
                explode=explode,
                shadow=True,
                textprops=dict(color="black")
            )
            ax.axis('equal')
            ax.legend(wedges, labels,
                      title="Sản phẩm",
                      loc="center left",
                      bbox_to_anchor=(1, 0, 0.5, 1))

        else:
            bars = ax.bar(labels, values, color=colors_bar, width=0.5)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            for bar in bars:
                yval = bar.get_height()
                if yval > 1000000:
                    display_val = f'{yval / 1000000:.1f}M'
                else:
                    display_val = f'{int(yval)}'

                ax.text(bar.get_x() + bar.get_width() / 2, yval, display_val,
                        va='bottom', ha='center', fontsize=9, fontweight='bold', color='#333')

            ax.set_xlabel(xlabel, fontsize=10)
            ax.set_ylabel(ylabel, fontsize=10)

            if len(labels) > 5:
                plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

        ax.set_title(title, fontsize=12, fontweight='bold', color='#005aae', pad=15)

        fig.tight_layout()
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_summary(self, rev, count, best_seller=None):
        self.lbl_total_revenue.config(text=f"{rev:,.0f} đ")
        self.lbl_total_orders.config(text=str(count))
        if best_seller:
            self.lbl_top_product.config(text=best_seller)

    def update_treeview(self, columns, data):
        self.result_tree.delete(*self.result_tree.get_children())
        self.result_tree['columns'] = columns
        self.result_tree['show'] = 'headings'

        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=150, anchor='center')

        for row in data:
            self.result_tree.insert("", "end", values=row)

    def show_stats_revenue_month(self):
        self.title_label.config(text="DOANH THU THEO THÁNG")
        data = self.controller.get_revenue_stats('month')

        self.update_summary(data['total_revenue'], data['total_orders'])
        self.draw_chart(data['labels'], data['values'],
                        "Xu hướng Doanh thu theo Tháng", "Thời gian", "Doanh thu (VNĐ)", 'bar')
        self.update_treeview(("Thời gian", "Số đơn hàng", "Doanh thu"), data['table_data'])

    def show_stats_revenue_quarter(self):
        self.title_label.config(text="DOANH THU THEO QUÝ")
        data = self.controller.get_revenue_stats('quarter')

        self.update_summary(data['total_revenue'], data['total_orders'])
        self.draw_chart(data['labels'], data['values'],
                        "Xu hướng Doanh thu theo Quý", "Quý", "Doanh thu (VNĐ)", 'bar')
        self.update_treeview(("Thời gian", "Số đơn hàng", "Doanh thu"), data['table_data'])

    def show_stats_revenue_year(self):
        self.title_label.config(text="DOANH THU THEO NĂM")
        data = self.controller.get_revenue_stats('year')

        self.update_summary(data['total_revenue'], data['total_orders'])
        self.draw_chart(data['labels'], data['values'],
                        "Tăng trưởng Doanh thu qua các Năm", "Năm", "Doanh thu (VNĐ)", 'bar')
        self.update_treeview(("Thời gian", "Số đơn hàng", "Doanh thu"), data['table_data'])

    def show_stats_top_products(self):
        self.title_label.config(text="TOP 5 SẢN PHẨM BÁN CHẠY (THEO DOANH THU)")
        data = self.controller.get_top_products_stats()
        self.lbl_top_product.config(text=data['best_seller'])
        self.lbl_total_revenue.config(text=f"{data['total_revenue']:,.0f} đ")
        self.lbl_total_orders.config(text=f"{data['total_qty']} ")
        self.draw_chart(data['labels'], data['values'],
                        "Tỷ trọng Doanh thu Top 5 Sản phẩm", "", "", 'pie')
        self.update_treeview(("#", "Tên Sản Phẩm", "Số lượng bán", "Doanh thu"), data['table_data'])

    def show_stats_custom_range(self):
        start = self.entry_start_date.get()
        end = self.entry_end_date.get()
        res = self.controller.get_custom_stats(start, end)
        if res:
            self.title_label.config(text=f"DOANH THU TỪ {start} ĐẾN {end}")
            self.update_summary(res['total_revenue'], res['total_orders'])
            if res['values']:
                self.draw_chart(res['labels'], res['values'],
                                f"Biểu đồ xu hướng doanh thu ({start} - {end})",
                                "Ngày", "Doanh thu (VNĐ)",
                                chart_type='line')

                self.update_treeview(("Ngày", "Số đơn hàng", "Doanh thu"), res['table_data'])
            else:
                if self.current_canvas: self.current_canvas.get_tk_widget().destroy()
                self.result_tree.delete(*self.result_tree.get_children())
                messagebox.showinfo("Thông báo", "Không tìm thấy dữ liệu doanh thu trong khoảng thời gian này.")

        else:
            messagebox.showerror("Lỗi", "Ngày tháng không hợp lệ hoặc lỗi định dạng.")

    def show_stats_products_top_quantity(self):
        self.title_label.config(text="TOP 5 SẢN PHẨM BÁN CHẠY (THEO SỐ LƯỢNG)")
        data = self.controller.get_top_products_quantity_stats()
        self.lbl_top_product.config(text=data['best_seller'])
        self.lbl_total_revenue.config(text=f"{data['total_revenue']:,.0f} đ")
        self.lbl_total_orders.config(text=f"{data['total_qty']} ")
        self.draw_chart(data['labels'], data['values'],
                        "So sánh Số lượng bán ra", "Sản phẩm", "Số lượng (Cái)", 'bar')

        self.update_treeview(("#", "Tên Sản Phẩm", "Số lượng bán", "Doanh thu mang lại"), data['table_data'])

    def refresh_current_stats(self):
        self.show_stats_revenue_month()
        messagebox.showinfo("Thông báo", "Dữ liệu đã được làm mới!", parent=self)

    def export_to_excel(self):
        try:
            import csv
            from tkinter import filedialog

            rows = self.result_tree.get_children()
            if not rows:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu để xuất!", parent=self)
                return

            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Lưu báo cáo thống kê"
            )

            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    columns = self.result_tree['columns']
                    writer.writerow(columns)
                    for row_id in rows:
                        row_data = self.result_tree.item(row_id)['values']
                        writer.writerow(row_data)

                messagebox.showinfo("Thành công", f"Đã xuất file tại:\n{file_path}", parent=self)

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file: {e}", parent=self)

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
