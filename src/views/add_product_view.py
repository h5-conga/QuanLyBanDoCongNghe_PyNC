import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from src.controllers.product_controller import ProductController


class AddProductWindow:
    def __init__(self, master, controller: ProductController):
        self.master = master
        self.controller = controller
        self.categories = self.controller.get_category_names()
        self.brands = self.controller.get_brand_names()
        self.img_path = None
        self.img_obj = None
        self.create_window()

    def create_window(self):
        self.win = tk.Toplevel(self.master)
        self.win.title("Thêm sản phẩm")
        self.win.geometry("800x500")
        self.win.resizable(False, False)
        self.win.configure(bg="#f5f5f5")
        self.win.grab_set()
        self.win.focus_force()

        main = tk.Frame(self.win, bg="#f5f5f5")
        main.pack(fill="both", expand=True, padx=15, pady=15)

        tk.Label(main, text="➕ Thêm sản phẩm", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(anchor="w")
        tk.Frame(main, height=2, bg="#4CAF50").pack(fill="x", pady=(0, 10))

        top_frame = tk.Frame(main, bg="#f5f5f5")
        top_frame.pack(fill="x", expand=False)

        inputs_frame = tk.Frame(top_frame, bg="#f5f5f5")
        inputs_frame.pack(side="left", fill="both", expand=True)

        wide_entry = 25
        medium_entry = 15
        padx_val = 5
        pady_val = 5

        row = 0
        tk.Label(inputs_frame, text="Tên sản phẩm", bg="#f5f5f5").grid(row=row, column=0, sticky="w", padx=padx_val,
                                                                       pady=pady_val)
        self.name_entry = tk.Entry(inputs_frame, width=wide_entry)
        self.name_entry.grid(row=row + 1, column=0, columnspan=2, sticky="we", padx=padx_val, pady=pady_val)

        tk.Label(inputs_frame, text="Số lượng", bg="#f5f5f5").grid(row=row, column=2, sticky="w", padx=padx_val,
                                                                   pady=pady_val)
        self.qty_entry = tk.Entry(inputs_frame, width=medium_entry)
        self.qty_entry.grid(row=row + 1, column=2, sticky="we", padx=padx_val, pady=pady_val)

        row += 2
        tk.Label(inputs_frame, text="Giá nhập (VNĐ)", bg="#f5f5f5").grid(row=row, column=0, sticky="w", padx=padx_val,
                                                                         pady=pady_val)
        self.import_entry = tk.Entry(inputs_frame, width=medium_entry)
        self.import_entry.grid(row=row + 1, column=0, sticky="we", padx=padx_val, pady=pady_val)

        tk.Label(inputs_frame, text="Giá bán (VNĐ)", bg="#f5f5f5").grid(row=row, column=1, sticky="w", padx=padx_val,
                                                                        pady=pady_val)
        self.price_entry = tk.Entry(inputs_frame, width=medium_entry)
        self.price_entry.grid(row=row + 1, column=1, sticky="we", padx=padx_val, pady=pady_val)

        tk.Label(inputs_frame, text="Bảo hành (tháng)", bg="#f5f5f5").grid(row=row, column=2, sticky="w", padx=padx_val,
                                                                           pady=pady_val)
        self.warranty_entry = tk.Entry(inputs_frame, width=medium_entry)
        self.warranty_entry.grid(row=row + 1, column=2, sticky="we", padx=padx_val, pady=pady_val)

        row += 2
        tk.Label(inputs_frame, text="Danh mục", bg="#f5f5f5").grid(row=row, column=0, sticky="w", padx=padx_val,
                                                                   pady=pady_val)
        self.cat_cb = ttk.Combobox(inputs_frame, values=self.categories, state="readonly", width=wide_entry)
        self.cat_cb.grid(row=row + 1, column=0, columnspan=2, sticky="we", padx=padx_val, pady=pady_val)

        tk.Label(inputs_frame, text="Thương hiệu", bg="#f5f5f5").grid(row=row, column=2, sticky="w", padx=padx_val,
                                                                      pady=pady_val)
        self.brand_cb = ttk.Combobox(inputs_frame, values=self.brands, state="readonly", width=medium_entry)
        self.brand_cb.grid(row=row + 1, column=2, sticky="we", padx=padx_val, pady=pady_val)

        for i in range(3):
            inputs_frame.grid_columnconfigure(i, weight=1)

        img_frame = tk.Frame(top_frame, width=200, bg="#f5f5f5")
        img_frame.pack(side="right", fill="y", padx=10)

        self.img_display = tk.Frame(img_frame, width=180, height=180, relief="solid", bd=1, bg="white")
        self.img_display.pack(pady=10)
        self.img_display.pack_propagate(False)

        self.placeholder = tk.Label(self.img_display, text="🖼\nDouble Click\nđể chọn ảnh", font=("Arial", 16),
                                    fg="#888", bg="white")
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

        self.img_display.bind("<Double-Button-1>", self.choose_image)
        self.placeholder.bind("<Double-Button-1>", self.choose_image)

        bottom_frame = tk.Frame(main, bg="#f5f5f5")
        bottom_frame.pack(fill="x", pady=(10, 0))

        tk.Label(bottom_frame, text="Mô tả", bg="#f5f5f5").pack(anchor="w")
        self.desc_text = tk.Text(bottom_frame, height=6, wrap="word", relief="solid", bd=1)
        self.desc_text.pack(fill="x", pady=(5, 5))

        btn_frame = tk.Frame(bottom_frame, bg="#f5f5f5")
        btn_frame.pack(anchor="e")
        tk.Button(btn_frame, text="Lưu", bg="#4CAF50", fg="white", padx=20, pady=7, relief="flat",
                  command=self.save_product).pack(side="right", padx=5)
        tk.Button(btn_frame, text="Hủy", bg="#f44336", fg="white", padx=20, pady=7, relief="flat",
                  command=self.win.destroy).pack(side="right", padx=5)

    def choose_image(self, event):
        filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        path = filedialog.askopenfilename(title="Chọn ảnh sản phẩm", filetypes=filetypes)
        if path:
            self.img_path = path
            img = Image.open(path)
            img.thumbnail((180, 180))
            self.img_obj = ImageTk.PhotoImage(img, master=self.win)
            self.placeholder.place_forget()
            if hasattr(self, 'img_label'):
                self.img_label.config(image=self.img_obj)
            else:
                self.img_label = tk.Label(self.img_display, image=self.img_obj, bg="white")
                self.img_label.place(relx=0.5, rely=0.5, anchor="center")
                self.img_label.bind("<Double-Button-1>", self.choose_image)
                self.del_btn = tk.Button(self.img_display, text="X", command=self.remove_image, bg="#f44336",
                                         fg="white", bd=0)
                self.del_btn.place(relx=1, rely=0, anchor="ne")

    def remove_image(self):
        self.img_path = None
        self.img_obj = None
        if hasattr(self, 'img_label'):
            self.img_label.destroy()
        if hasattr(self, 'del_btn'):
            self.del_btn.destroy()
        self.placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def save_product(self):
        try:
            data = {
                "name": self.name_entry.get(),
                "category_name": self.cat_cb.get(),
                "brand_name": self.brand_cb.get(),
                "description": self.desc_text.get("1.0", "end-1c").strip(),
                "image_path": self.img_path,
                "quantity": int(self.qty_entry.get()),
                "price": float(self.price_entry.get()),
                "cost_price": float(self.import_entry.get()),
                "warranty": int(self.warranty_entry.get()),
            }
        except ValueError:
            messagebox.showwarning("Dữ liệu không hợp lệ",
                                   "Vui lòng đảm bảo các ô Số lượng, Giá, và Bảo hành là SỐ và không bị bỏ trống.",
                                   parent=self.win)
            return
        if not all([data['name'], data['category_name'], data['brand_name']]):
            messagebox.showwarning("Thiếu thông tin",
                                   "Vui lòng điền đầy đủ Tên, Danh mục và Thương hiệu.",
                                   parent=self.win)
            return
        success, message = self.controller.handle_add_product(data)

        if success:
            messagebox.showinfo("Thành công", message, parent=self.win)
            self.win.destroy()
        else:
            messagebox.showerror("Lỗi", message, parent=self.win)