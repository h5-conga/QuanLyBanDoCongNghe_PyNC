import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.account_controller import AccountController
from src.views.create_account_view import CreateAccountView


class AccountView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#f0f0f0")
        self.controller = AccountController()
        self.pack(fill=tk.BOTH, expand=True)

        self.create_layout()
        self.load_data()

    def create_layout(self):
        header = tk.Frame(self, bg="white", height=60)
        header.pack(fill="x", pady=(0, 10))
        tk.Label(header, text="QUẢN LÝ TÀI KHOẢN", font=("Segoe UI", 18, "bold"), fg="#333", bg="white").pack(
            side="left", padx=20, pady=10)

        toolbar = tk.Frame(self, bg="#f0f0f0")
        toolbar.pack(fill="x", padx=20, pady=5)

        tk.Button(toolbar, text="Thêm Tài Khoản", bg="#4CAF50", fg="white", font=("Segoe UI", 10, "bold"),
                  bd=0, padx=15, pady=8, command=self.open_add_user).pack(side="left")

        tk.Button(toolbar, text="Khóa / Mở Khóa", bg="#FF9800", fg="white", font=("Segoe UI", 10, "bold"),
                  bd=0, padx=15, pady=8, command=self.on_toggle_click).pack(side="left", padx=10)

        tk.Button(toolbar, text="Tải lại", bg="#2196F3", fg="white", font=("Segoe UI", 10, "bold"),
                  bd=0, padx=15, pady=8, command=self.load_data).pack(side="right")

        tree_frame = tk.Frame(self, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("ID", "Username", "Họ Tên", "Vai Trò", "Trạng Thái")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.heading("Username", text="Tên đăng nhập")
        self.tree.column("Username", width=150)
        self.tree.heading("Họ Tên", text="Họ và Tên")
        self.tree.column("Họ Tên", width=200)
        self.tree.heading("Vai Trò", text="Vai Trò")
        self.tree.column("Vai Trò", width=100, anchor="center")
        self.tree.heading("Trạng Thái", text="Trạng Thái")
        self.tree.column("Trạng Thái", width=100, anchor="center")

        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.tag_configure("locked", background="#FFEBEE", foreground="#D32F2F")  # Đỏ nhạt
        self.tree.tag_configure("active", background="white", foreground="black")

    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        users = self.controller.get_all_users_view()
        for u in users:
            tag = "locked" if u['status'] == 'locked' else "active"
            self.tree.insert("", "end", values=(
                u['id'], u['username'], u['fullname'], u['role'].upper(), u['status'].upper()
            ), tags=(tag,))

    def open_add_user(self):
        CreateAccountView(self.winfo_toplevel(), self.controller, self.load_data)

    def on_toggle_click(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một tài khoản để khóa/mở khóa.")
            return

        item = self.tree.item(sel[0])
        target_user_id = item['values'][0]
        username = item['values'][1]
        current_status = item['values'][4]

        current_admin_id = None
        try:
            parent = self.master
            while parent:
                if hasattr(parent, 'current_user_id'):
                    current_admin_id = parent.current_user_id
                    break
                if hasattr(parent, 'current_user') and parent.current_user:
                    current_admin_id = parent.current_user.user_id
                    break
                parent = parent.master
        except Exception:
            pass
        if current_admin_id is not None and str(target_user_id) == str(current_admin_id):
            messagebox.showerror("Cấm", "Bạn không thể khóa chính tài khoản mình đang sử dụng!")
            return
        action = "KHÓA" if current_status == "ACTIVE" else "MỞ KHÓA"
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn {action} tài khoản '{username}'?"):
            success, msg = self.controller.toggle_status(target_user_id, current_user_id=current_admin_id)

            if success:
                messagebox.showinfo("Thành công", msg)
                self.load_data()
            else:
                messagebox.showerror("Lỗi", msg)