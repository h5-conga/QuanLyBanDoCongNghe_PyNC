import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from src.models.entity import Product
from src.controllers.product_controller import ProductController
from src.views.edit_product_view import EditProductWindow


class ProductDetailsWindow:
    def __init__(self, master, product: Product, controller: ProductController, role='user'):
        self.master = master
        self.product = product
        self.controller = controller
        self.role = role
        self.image_obj = None
        self.create_widgets()

    def create_widgets(self):
        self.win = tk.Toplevel(self.master)
        self.win.title(f"Chi tiết: {self.product.product_name}")
        self.win.geometry("800x500")
        self.win.resizable(False, False)
        self.win.configure(bg="#f5f5f5")

        self.win.grab_set()
        self.win.focus_force()

        main = tk.Frame(self.win, bg="#f5f5f5")
        main.pack(fill="both", expand=True, padx=15, pady=15)
        tk.Label(main, text="CHI TIẾT SẢN PHẨM", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(anchor="w")
        tk.Frame(main, height=2, bg="#2196F3").pack(fill="x", pady=(0, 10))

        top_frame = tk.Frame(main, bg="#f5f5f5")
        top_frame.pack(fill="x", pady=(0, 10))
        info_frame = tk.Frame(top_frame, bg="#f5f5f5")
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        tk.Label(info_frame, text="ID Sản phẩm (DB):", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=0, column=0,
                                                                                                      sticky="w",
                                                                                                      pady=4)
        tk.Label(info_frame, text=self.product.product_id, font=("Arial", 11), bg="#f5f5f5").grid(row=0, column=1,
                                                                                                  sticky="w", pady=4)
        tk.Label(info_frame, text="Tên:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=0, column=2, sticky="w",
                                                                                         pady=4)
        tk.Label(info_frame, text=self.product.product_name, font=("Arial", 11), bg="#f5f5f5", wraplength=250).grid(
            row=0, column=3, sticky="w", pady=4, columnspan=3)

        tk.Label(info_frame, text="Số lượng:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=1, column=0,
                                                                                              sticky="w", pady=4)
        tk.Label(info_frame, text=self.product.stock_quantity, font=("Arial", 11), bg="#f5f5f5").grid(row=1, column=1,
                                                                                                      sticky="w",
                                                                                                      pady=4)
        tk.Label(info_frame, text="Giá bán:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=1, column=2,
                                                                                             sticky="w", pady=4)
        tk.Label(info_frame, text=f"{self.product.price:,.2f} VNĐ", font=("Arial", 11), bg="#f5f5f5").grid(row=1,
                                                                                                           column=3,
                                                                                                           sticky="w",
                                                                                                           pady=4)

        if self.role == "admin":
            tk.Label(info_frame, text="Giá nhập:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=1, column=4,
                                                                                                  sticky="w", pady=4)
            tk.Label(info_frame, text=f"{self.product.cost_price:,.2f} VNĐ", font=("Arial", 11), bg="#f5f5f5").grid(
                row=1, column=5, sticky="w", pady=4)

        tk.Label(info_frame, text="Thời gian bảo hành:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=2, column=0,
                                                                                                        sticky="w",
                                                                                                        pady=4)
        tk.Label(info_frame, text=f"{self.product.warranty_date} tháng", font=("Arial", 11), bg="#f5f5f5").grid(row=2,
                                                                                                                column=1,
                                                                                                                sticky="w",
                                                                                                                pady=4)
        tk.Label(info_frame, text="Ngày nhập:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=2, column=2,
                                                                                               sticky="w", pady=4)
        entry_date_str = self.product.entry_date.strftime("%d/%m/%Y") if self.product.entry_date else "Chưa có"
        tk.Label(info_frame, text=entry_date_str, font=("Arial", 11), bg="#f5f5f5").grid(row=2, column=3, sticky="w",
                                                                                         pady=4)
        brand_name = self.controller.brand_map.get(self.product.brand_id, "N/A")
        cat_name = self.controller.category_map.get(self.product.category_id, "N/A")

        tk.Label(info_frame, text="Thương hiệu", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=3, column=0,
                                                                                                sticky="w", pady=4)
        tk.Label(info_frame, text=brand_name, font=("Arial", 11), bg="#f5f5f5").grid(row=3, column=1, sticky="w",
                                                                                     pady=4)
        tk.Label(info_frame, text="Danh mục", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=3, column=2,
                                                                                             sticky="w", pady=4)
        tk.Label(info_frame, text=cat_name, font=("Arial", 11), bg="#f5f5f5").grid(row=3, column=3, sticky="w", pady=4)

        for i in range(6):
            info_frame.grid_columnconfigure(i, weight=1)
        img_frame = tk.Frame(top_frame, bg="#f5f5f5", width=200)
        img_frame.pack(side="right", fill="y")
        img_box = tk.Frame(img_frame, width=180, height=180, relief="solid", bd=1, bg="white")
        img_box.pack(pady=10)
        img_box.pack_propagate(False)

        image_list = self.controller.product_service.get_images_of_product(self.product.product_id)

        img_path = None
        if image_list:
            img_path = image_list[0]['image_path']

        if img_path and os.path.exists(img_path):
            try:
                img = Image.open(img_path)
                img.thumbnail((180, 180))
                self.image_obj = ImageTk.PhotoImage(img, master=self.win)
                img_label = tk.Label(img_box, image=self.image_obj, bg="white")
                img_label.place(relx=0.5, rely=0.5, anchor="center")
            except Exception as e:
                print(f"Lỗi tải ảnh: {e}")
                tk.Label(img_box, text="🖼\nLỗi ảnh", font=("Arial", 14), fg="red", bg="white").place(relx=0.5, rely=0.5,
                                                                                                     anchor="center")
        else:
            tk.Label(img_box, text="🖼\nKhông có ảnh", font=("Arial", 14), fg="#888", bg="white").place(relx=0.5,
                                                                                                       rely=0.5,
                                                                                                       anchor="center")
            if img_path:
                print(f"[Debug] Không tìm thấy file ảnh tại đường dẫn gốc: {img_path}")

        bottom_frame = tk.Frame(main, bg="#f5f5f5")
        bottom_frame.pack(fill="both", expand=True)

        tk.Label(bottom_frame, text="Mô tả sản phẩm", font=("Arial", 11, "bold"), bg="#f5f5f5").pack(anchor="w")
        desc_box = tk.Text(bottom_frame, height=6, wrap="word", relief="solid", bd=1)
        desc_box.pack(fill="both", expand=True, pady=5)
        desc_box.insert("1.0", self.product.description)
        desc_box.config(state="disabled")

        btn_frame = tk.Frame(bottom_frame, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=10)

        if self.role == "admin":
            ttk.Button(btn_frame, text="Sửa sản phẩm", command=self.edit_product).pack(side="left")

        ttk.Button(btn_frame, text="Đóng", command=self.win.destroy).pack(side="right")

    def edit_product(self):
        # 1. Mở cửa sổ Edit
        edit_win = EditProductWindow(self.master, self.product, self.controller)

        # 2. Quan trọng: Chờ cửa sổ Edit đóng lại (User ấn Lưu hoặc Hủy)
        self.win.wait_window(edit_win.win)

        # 3. Sau khi Edit xong, đóng cửa sổ Detail này.
        # Lúc này ProductView sẽ nhận được tín hiệu là Detail đã đóng -> Tự động refresh
        self.win.destroy()