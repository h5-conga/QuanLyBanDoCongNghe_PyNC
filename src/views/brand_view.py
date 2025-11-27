import tkinter as tk
from tkinter import messagebox
from src.models.entity import Brand


class BrandView(tk.Toplevel):
    def __init__(self, parent, brand: Brand, controller, role='user', refresh_callback=None):
        super().__init__(parent)
        self.title(f"Chi tiết thương hiệu: {brand.brand_name}")
        self.geometry("400x350")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        self.brand = brand
        self.controller = controller
        self.role = role
        self.refresh_callback = refresh_callback
        self.is_editing = False
        self.setup_ui()
        self.load_data()
        self.lock_fields()

    def setup_ui(self):
        main_frame = tk.Frame(self, bg="#f5f5f5")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_columnconfigure(1, weight=1)
        tk.Label(main_frame, text="ID:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w",
                                                                                        pady=5)
        self.entry_id = tk.Entry(main_frame, width=40, bg="#e0e0e0")
        self.entry_id.grid(row=0, column=1, sticky="we", pady=5)
        tk.Label(main_frame, text="Tên thương hiệu:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=1, column=0,
                                                                                                     sticky="w", pady=5)
        self.entry_name = tk.Entry(main_frame, width=40)
        self.entry_name.grid(row=1, column=1, sticky="we", pady=5)
        tk.Label(main_frame, text="Quốc gia:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=2, column=0,
                                                                                              sticky="w", pady=5)
        self.entry_country = tk.Entry(main_frame, width=40)
        self.entry_country.grid(row=2, column=1, sticky="we", pady=5)
        tk.Label(main_frame, text="Mô tả:", bg="#f5f5f5", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="nw",
                                                                                           pady=5)
        self.txt_desc = tk.Text(main_frame, height=5, width=30, relief="solid", bd=1)
        self.txt_desc.grid(row=3, column=1, sticky="we", pady=5)
        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=15)
        tk.Button(btn_frame, text="Đóng", command=self.destroy, bg="#999", fg="white", padx=15).pack(side="right")
        if self.role == 'admin':
            self.btn_edit = tk.Button(btn_frame, text="Sửa", command=self.toggle_edit, bg="#2196F3", fg="white",
                                      padx=15)
            self.btn_edit.pack(side="right", padx=10)

    def load_data(self):
        self.entry_id.insert(0, str(self.brand.brand_id))
        self.entry_name.insert(0, self.brand.brand_name)
        self.entry_country.insert(0, self.brand.country if self.brand.country else "")
        self.txt_desc.insert("1.0", self.brand.brand_des if self.brand.brand_des else "")

    def lock_fields(self):
        self.entry_id.config(state="readonly")
        self.entry_name.config(state="readonly")
        self.entry_country.config(state="readonly")
        self.txt_desc.config(state="disabled")

    def unlock_fields(self):
        self.entry_name.config(state="normal")
        self.entry_country.config(state="normal")
        self.txt_desc.config(state="normal")

    def toggle_edit(self):
        if not self.is_editing:
            self.is_editing = True
            self.unlock_fields()
            self.btn_edit.config(text="Lưu", bg="#4CAF50")
            self.entry_name.focus()
        else:
            self.save_changes()

    def save_changes(self):
        new_name = self.entry_name.get().strip()
        new_country = self.entry_country.get().strip()
        new_desc = self.txt_desc.get("1.0", "end-1c").strip()
        if not new_name:
            messagebox.showwarning("Cảnh báo", "Tên thương hiệu không được để trống", parent=self)
            return
        self.brand.brand_name = new_name
        self.brand.country = new_country
        self.brand.brand_des = new_desc
        success, msg = self.controller.handle_update_brand(self.brand)
        if success:
            messagebox.showinfo("Thành công", msg, parent=self)
            self.is_editing = False
            self.lock_fields()
            self.btn_edit.config(text="Sửa", bg="#2196F3")
            if self.refresh_callback:
                self.refresh_callback()
        else:
            messagebox.showerror("Lỗi", msg, parent=self)