import tkinter as tk
from tkinter import messagebox


class AddCustomerView(tk.Toplevel):
    def __init__(self, parent, controller, callback_refresh):
        super().__init__(parent)
        self.controller = controller
        self.callback_refresh = callback_refresh

        self.title("Thêm Khách Hàng Mới")
        self.geometry("450x500")
        self.configure(bg="#F0F2F5")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.center_window()
        self.create_widgets()
        self.entry_name.focus_set()
        self.bind('<Return>', lambda event: self.save_action())
        self.bind('<Escape>', lambda event: self.destroy())

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        header_frame = tk.Frame(self, bg="#1976D2", height=60)
        header_frame.pack(side="top", fill="x")
        header_frame.pack_propagate(False)
        lbl_title = tk.Label(header_frame, text="THÊM KHÁCH HÀNG",
                             font=("Segoe UI", 14, "bold"), fg="white", bg="#1976D2")
        lbl_title.pack(side="left", padx=20, pady=10)

        card_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        card_frame.configure(highlightbackground="#E0E0E0", highlightthickness=1, bd=0)
        card_frame.pack(padx=20, pady=20, fill="both", expand=True)
        lbl_font = ("Segoe UI", 10, "bold")
        entry_font = ("Segoe UI", 11)
        def create_field(row, label_text, is_required=False):
            lbl_text = label_text + (" (*)" if is_required else "")
            fg_color = "#D32F2F" if is_required else "#333333"
            tk.Label(card_frame, text=lbl_text, font=lbl_font, bg="white", fg="#555").grid(
                row=row, column=0, sticky="w", padx=20, pady=(15, 5))
            entry = tk.Entry(card_frame, font=entry_font, bg="#FAFAFA",
                             bd=1, relief="solid", highlightthickness=1, highlightcolor="#2196F3")
            entry.grid(row=row + 1, column=0, sticky="ew", padx=20, ipady=5)
            return entry
        card_frame.grid_columnconfigure(0, weight=1)
        self.entry_name = create_field(0, "Họ và tên", is_required=True)
        self.entry_phone = create_field(2, "Số điện thoại", is_required=True)
        self.entry_email = create_field(4, "Email")
        self.entry_address = create_field(6, "Địa chỉ")
        btn_frame = tk.Frame(self, bg="#F0F2F5")
        btn_frame.pack(side="bottom", fill="x", pady=20, padx=20)
        btn_cancel = tk.Button(btn_frame, text="Hủy bỏ", font=("Segoe UI", 10),
                               bg="#E0E0E0", fg="#333", bd=0, padx=15, pady=8, cursor="hand2",
                               command=self.destroy)
        btn_cancel.pack(side="right", padx=(10, 0))
        btn_save = tk.Button(btn_frame, text="Lưu Khách Hàng", font=("Segoe UI", 10, "bold"),
                             bg="#4CAF50", fg="white", bd=0, padx=20, pady=8, cursor="hand2",
                             activebackground="#43A047",
                             command=self.save_action)
        btn_save.pack(side="right")

    def save_action(self):
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()
        address = self.entry_address.get().strip()
        if not name:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Tên khách hàng!", parent=self)
            self.entry_name.focus()
            return

        if not phone:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Số điện thoại!", parent=self)
            self.entry_phone.focus()
            return
        success, message = self.controller.handle_add_customer(name, phone, email, address)

        if success:
            messagebox.showinfo("Thành công", message, parent=self)
            if self.callback_refresh:
                self.callback_refresh()
            self.destroy()
        else:
            messagebox.showerror("Lỗi", message, parent=self)