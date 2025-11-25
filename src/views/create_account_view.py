import tkinter as tk
from tkinter import ttk, messagebox
from src.models.Enum import Role_Enum, Status_user_Enum


class CreateAccountView(tk.Toplevel):
    def __init__(self, parent, controller, callback_refresh):
        super().__init__(parent)
        self.controller = controller
        self.callback_refresh = callback_refresh

        self.title("Thêm Tài Khoản Mới")
        self.geometry("450x580")
        self.configure(bg="#F0F2F5")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.center_window()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        header = tk.Frame(self, bg="#2196F3", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="THÊM TÀI KHOẢN", font=("Segoe UI", 14, "bold"), fg="white", bg="#2196F3").pack(pady=15)
        card = tk.Frame(self, bg="white", bd=1, relief="solid")
        card.configure(highlightbackground="#E0E0E0", highlightthickness=1, bd=0)
        card.pack(padx=20, pady=20, fill="both", expand=True)
        card.grid_columnconfigure(0, weight=1)
        font_lbl = ("Segoe UI", 10, "bold")
        font_ent = ("Segoe UI", 11)

        def make_entry(row, label, is_password=False):
            tk.Label(card, text=label + " (*)", font=font_lbl, bg="white", fg="#333").grid(row=row, column=0,
                                                                                           sticky="w", padx=20,
                                                                                           pady=(10, 5))
            ent = tk.Entry(card, font=font_ent, bg="#FAFAFA", relief="solid", bd=1, show="*" if is_password else "")
            ent.grid(row=row + 1, column=0, sticky="ew", padx=20, ipady=5)
            return ent

        self.ent_user = make_entry(0, "Tên đăng nhập")
        self.ent_pass = make_entry(2, "Mật khẩu", is_password=True)
        self.ent_name = make_entry(4, "Họ và tên")

        tk.Label(card, text="Vai trò (*)", font=font_lbl, bg="white").grid(row=6, column=0, sticky="w", padx=20,
                                                                           pady=(10, 5))
        self.cb_role = ttk.Combobox(card, values=[e.value for e in Role_Enum], state="readonly", font=font_ent)
        self.cb_role.grid(row=7, column=0, sticky="ew", padx=20, ipady=5)
        self.cb_role.current(1)

        tk.Label(card, text="Trạng thái (*)", font=font_lbl, bg="white").grid(row=8, column=0, sticky="w", padx=20,
                                                                              pady=(10, 5))
        self.cb_status = ttk.Combobox(card, values=[e.value for e in Status_user_Enum], state="readonly", font=font_ent)
        self.cb_status.grid(row=9, column=0, sticky="ew", padx=20, ipady=5)
        self.cb_status.set(Status_user_Enum.ACTIVE.value)

        btn_frame = tk.Frame(self, bg="#F0F2F5")
        btn_frame.pack(side="bottom", fill="x", pady=20, padx=20)

        tk.Button(btn_frame, text="Hủy", command=self.destroy, bg="#E0E0E0", bd=0, padx=15, pady=8).pack(side="right",
                                                                                                         padx=(10, 0))
        tk.Button(btn_frame, text="Lưu Tài Khoản", command=self.save_action, bg="#4CAF50", fg="white",
                  font=("Segoe UI", 10, "bold"), bd=0, padx=20, pady=8).pack(side="right")

    def save_action(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        n = self.ent_name.get().strip()
        r = self.cb_role.get()
        s = self.cb_status.get()

        success, msg = self.controller.add_new_user(u, p, n, r, s)
        if success:
            messagebox.showinfo("Thành công", msg)
            if self.callback_refresh: self.callback_refresh()
            self.destroy()
        else:
            messagebox.showerror("Thất bại", msg)