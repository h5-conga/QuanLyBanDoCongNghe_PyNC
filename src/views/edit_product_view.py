import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
from src.models.entity import Product
from src.controllers.product_controller import ProductController


class EditProductWindow:
    def __init__(self, master, product: Product, controller: ProductController):
        self.master = master
        self.product = product
        self.controller = controller
        self.categories = self.controller.get_category_names()
        self.brands = self.controller.get_brand_names()
        self.img_path = None
        self.img_obj = None
        self.entries = {}
        self.build_window()

    def build_window(self):
        self.win = tk.Toplevel(self.master)
        self.win.title(f"Sửa sản phẩm - {self.product.product_name}")
        self.win.geometry("800x520")
        self.win.resizable(False, False)
        self.win.configure(bg="#f5f5f5")

        self.win.grab_set()
        self.win.focus_force()

        main = tk.Frame(self.win, bg="#f5f5f5")
        main.pack(fill="both", expand=True, padx=15, pady=15)
        tk.Label(main, text="Sửa sản phẩm", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(anchor="w")
        tk.Frame(main, height=2, bg="#FF9800").pack(fill="x", pady=(0, 10))
        top_frame = tk.Frame(main, bg="#f5f5f5")
        top_frame.pack(fill="x", pady=(0, 10))
        form_frame = tk.Frame(top_frame, bg="#f5f5f5")
        form_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        labels_map = {
            "Tên sản phẩm:": "product_name",
            "Số lượng:": "stock_quantity",
            "Giá bán (VNĐ):": "price",
            "Giá nhập (VNĐ):": "cost_price",
            "Bảo hành (tháng):": "warranty_date"
        }

        for i, (label, attr_name) in enumerate(labels_map.items()):
            tk.Label(form_frame, text=label, font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=i, column=0, sticky="w",
                                                                                            pady=4)
            e = tk.Entry(form_frame)
            e.grid(row=i, column=1, sticky="we", pady=4)
            val = getattr(self.product, attr_name)
            e.insert(0, str(val) if val is not None else "")
            self.entries[label] = e

        tk.Label(form_frame, text="Danh mục:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=5, column=0,
                                                                                              sticky="w", pady=4)
        self.cat_cb = ttk.Combobox(form_frame, values=self.categories, state="readonly")
        self.cat_cb.grid(row=5, column=1, sticky="we", pady=4)
        cat_name = self.controller.category_map.get(self.product.category_id, "")
        self.cat_cb.set(cat_name)

        tk.Label(form_frame, text="Thương hiệu:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=6, column=0,
                                                                                                 sticky="w", pady=4)
        self.brand_cb = ttk.Combobox(form_frame, values=self.brands, state="readonly")
        self.brand_cb.grid(row=6, column=1, sticky="we", pady=4)
        brand_name = self.controller.brand_map.get(self.product.brand_id, "")
        self.brand_cb.set(brand_name)

        tk.Label(form_frame, text="Ngày nhập:", font=("Arial", 11, "bold"), bg="#f5f5f5").grid(row=7, column=0,
                                                                                               sticky="w", pady=4)
        entry_date_str = self.product.entry_date.strftime("%d/%m/%Y") if self.product.entry_date else "Chưa có"
        tk.Label(form_frame, text=entry_date_str, font=("Arial", 11), bg="#f5f5f5").grid(row=7, column=1, sticky="w",
                                                                                         pady=4)

        form_frame.grid_columnconfigure(1, weight=1)

        img_frame = tk.Frame(top_frame, bg="#f5f5f5", width=200)
        img_frame.pack(side="right", fill="y")
        self.img_box = tk.Frame(img_frame, width=180, height=180, relief="solid", bd=1, bg="white")
        self.img_box.pack(pady=10)
        self.img_box.pack_propagate(False)
        self.load_current_image()
        tk.Button(img_frame, text="Thay đổi ảnh", command=self.choose_image, bg="#2196F3", fg="white",
                  relief="flat").pack(pady=5)

        bottom_frame = tk.Frame(main, bg="#f5f5f5")
        bottom_frame.pack(fill="both", expand=True)

        tk.Label(bottom_frame, text="Mô tả sản phẩm:", font=("Arial", 11, "bold"), bg="#f5f5f5").pack(anchor="w")
        self.desc_text = tk.Text(bottom_frame, height=6, wrap="word", relief="solid", bd=1)
        self.desc_text.pack(fill="both", expand=True, pady=5)
        if self.product.description:
            self.desc_text.insert("1.0", self.product.description)

        btn_frame = tk.Frame(bottom_frame, bg="#f5f5f5")
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="Lưu", bg="#4CAF50", fg="white", padx=20, pady=7, relief="flat",
                  command=self.save_product).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Hủy", bg="#f44336", fg="white", padx=20, pady=7, relief="flat",
                  command=self.win.destroy).pack(side="right", padx=5)

    def _display_image_from_path(self, image_path: str):
        for widget in self.img_box.winfo_children():
            widget.destroy()

        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img.thumbnail((180, 180))
                self.img_obj = ImageTk.PhotoImage(img, master=self.win)
                img_label = tk.Label(self.img_box, image=self.img_obj, bg="white")
                img_label.place(relx=0.5, rely=0.5, anchor="center")
                img_label.bind("<Double-Button-1>", self.choose_image)
            except Exception as e:
                print(f"Lỗi tải ảnh: {e}")
                tk.Label(self.img_box, text="🖼\nLỗi ảnh", font=("Arial", 14), fg="red", bg="white").place(relx=0.5,
                                                                                                          rely=0.5,
                                                                                                          anchor="center")
        else:
            placeholder = tk.Label(self.img_box, text="🖼\nKhông có ảnh", font=("Arial", 14), fg="#888", bg="white")
            placeholder.place(relx=0.5, rely=0.5, anchor="center")
            placeholder.bind("<Double-Button-1>", self.choose_image)

    def load_current_image(self):
        image_list = self.controller.get_images_of_product(self.product.product_id)
        img_filename = None
        if image_list:
            img_filename = image_list[0]['image_path']
        img_path = None
        if img_filename:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_path = os.path.join(base_dir, "images", img_filename)
        self._display_image_from_path(img_path)

    def choose_image(self, event=None):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        path = filedialog.askopenfilename(title="Chọn ảnh sản phẩm mới", filetypes=filetypes)
        if path:
            self.img_path = path
            self._display_image_from_path(path)

    def save_product(self):
        try:
            name = self.entries["Tên sản phẩm:"].get().strip()
            stock = self.entries["Số lượng:"].get().strip()
            price = self.entries["Giá bán (VNĐ):"].get().strip()
            cost_price = self.entries["Giá nhập (VNĐ):"].get().strip()
            warranty = self.entries["Bảo hành (tháng):"].get().strip()
            desc = self.desc_text.get("1.0", "end-1c").strip()
            cat_name = self.cat_cb.get()
            brand_name = self.brand_cb.get()

            if not all([name, cat_name, brand_name]):
                messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ Tên, Danh mục và Thương hiệu.",
                                       parent=self.win)
                return

            cat_id = next((k for k, v in self.controller.category_map.items() if v == cat_name), None)
            brand_id = next((k for k, v in self.controller.brand_map.items() if v == brand_name), None)

            if cat_id is None:
                messagebox.showerror("Lỗi", "Danh mục không hợp lệ", parent=self.win)
                return
            if brand_id is None:
                messagebox.showerror("Lỗi", "Thương hiệu không hợp lệ", parent=self.win)
                return

            self.product.product_name = name
            self.product.stock_quantity = int(stock)
            self.product.price = float(price)
            self.product.cost_price = float(cost_price)
            self.product.warranty_date = int(warranty)
            self.product.description = desc
            self.product.category_id = cat_id
            self.product.brand_id = brand_id

            success, message = self.controller.handle_update_product(self.product)

            if success:
                if self.img_path:
                    self.controller.add_image_for_product(self.product.product_id, self.img_path)
                messagebox.showinfo("Thành công", message, parent=self.win)
                self.win.destroy()
            else:
                messagebox.showerror("Lỗi", message, parent=self.win)

        except ValueError:
            messagebox.showwarning("Dữ liệu không hợp lệ",
                                   "Vui lòng đảm bảo các ô Số lượng, Giá, và Bảo hành là SỐ và không bị bỏ trống.",
                                   parent=self.win)