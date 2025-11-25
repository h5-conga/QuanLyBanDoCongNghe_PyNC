import tkinter as tk
from tkinter import ttk
import math

class StockCheckView(tk.Toplevel):
    def __init__(self, master, out_stock_list, near_out_of_stock_list):
        super().__init__(master)
        self.title("Cảnh báo Tồn kho")
        self.geometry("850x520")
        self.resizable(False, False)
        style = ttk.Style()
        style.configure("Treeview", rowheight=30, font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 11, 'bold'))
        tk.Label(self, text="BÁO CÁO TỒN KHO", font=("Arial", 16, "bold"), fg="#333").pack(pady=10)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)
        self._create_tab(notebook, out_stock_list, "Đã hết hàng", "#D32F2F")
        self._create_tab(notebook, near_out_of_stock_list, "Sắp hết hàng", "#F57C00")

    def _create_tab(self, notebook, data, title, color):
        frame = tk.Frame(notebook)
        notebook.add(frame, text=f"{title} ({len(data)})")
        cols = ("id", "name", "qty", "price")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        tree.column("id", width=60, anchor="center"); tree.heading("id", text="ID")
        tree.column("name", width=380);               tree.heading("name", text="Tên sản phẩm")
        tree.column("qty", width=100, anchor="center"); tree.heading("qty", text="SL Tồn")
        tree.column("price", width=150, anchor="e");  tree.heading("price", text="Giá bán")
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        tree.tag_configure("highlight", foreground=color, font=("Arial", 10, "bold"))
        tree.tag_configure("odd", background="#f9f9f9")
        tree.tag_configure("even", background="#ffffff")
        pagination_frame = tk.Frame(frame)
        pagination_frame.pack(fill="x", pady=5, padx=5)
        btn_next = tk.Button(pagination_frame, text=">", bd=0, relief="solid", width=3)
        lbl_page_info = tk.Label(pagination_frame, text="Trang 1 / 1", font=("Arial", 10))
        btn_prev = tk.Button(pagination_frame, text="<", bd=0, relief="solid", width=3)
        items_per_page = 10
        total_pages = max(1, math.ceil(len(data) / items_per_page))
        current_page = [1]

        def load_page(page):
            page = max(1, min(page, total_pages))
            current_page[0] = page
            tree.delete(*tree.get_children())
            start = (page - 1) * items_per_page
            end = page * items_per_page
            for i, p in enumerate(data[start:end]):
                bg_tag = "even" if i % 2 == 0 else "odd"
                tree.insert("", "end", values=(
                    p.product_id, p.product_name, p.stock_quantity, f"{p.price:,.0f} VNĐ"
                ), tags=("highlight", bg_tag))
            lbl_page_info.config(text=f"Trang {page} / {total_pages}")
            btn_prev.config(state="normal" if page > 1 else "disabled")
            btn_next.config(state="normal" if page < total_pages else "disabled")
        btn_prev.config(command=lambda: load_page(current_page[0] - 1))
        btn_next.config(command=lambda: load_page(current_page[0] + 1))

        btn_next.pack(side=tk.RIGHT, padx=5)
        lbl_page_info.pack(side=tk.RIGHT, padx=10)
        btn_prev.pack(side=tk.RIGHT, padx=5)
        load_page(1)