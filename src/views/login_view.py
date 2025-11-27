import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk

from src.services.auth_service import AuthService
from src.services.user_service import UserService


class LoginView(tk.Tk):
    def __init__(self, auth_service: AuthService, user_service: UserService):
        super().__init__()
        self.title("Đăng nhập hệ thống")
        self.geometry("1024x768")
        self.state('zoomed')

        self.auth_service = auth_service
        self.user_service = user_service

        self.BG_COLOR = "#ffffff"
        self.BTN_COLOR = "#007bff"
        self.BTN_ACTIVE = "#0056b3"
        self.TEXT_COLOR = "#333333"
        self.PLACEHOLDER_COLOR = "#888888"

        self.font_normal = tkFont.Font(family="Arial", size=10)
        self.font_bold = tkFont.Font(family="Arial", size=10, weight="bold")
        self.font_title = tkFont.Font(family="Arial", size=16, weight="bold")
        self.font_logo = tkFont.Font(family="Arial", size=14, weight="bold")

        self.load_background()
        self.create_widgets()

    def load_background(self):
        try:
            image = Image.open(r"D:\python\BTL\images\sapa-ruong-bac-thang.jpg")
            image = image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
            self.bg_image_tk = ImageTk.PhotoImage(image)
            bg_label = tk.Label(self, image=self.bg_image_tk)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Lỗi tải ảnh nền: {e}")
            self.config(bg="#333333")

    def create_widgets(self):
        login_frame = tk.Frame(self, bg=self.BG_COLOR, bd=1, relief="solid", borderwidth=0)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=380, height=350)

        logo_label = tk.Label(login_frame, text="Nhóm 14",
                              font=self.font_logo,
                              fg=self.BTN_COLOR,
                              bg=self.BG_COLOR)
        logo_label.pack(pady=(40, 0))

        title_label = tk.Label(login_frame, text="Đăng nhập",
                               font=self.font_title,
                               fg=self.TEXT_COLOR,
                               bg=self.BG_COLOR)
        title_label.pack(pady=(10, 30))

        self.placeholder_user = "Tên đăng nhập"
        user_frame, self.entry_user = self.create_entry_with_icon(
            login_frame, "👤", self.placeholder_user)
        user_frame.pack(fill="x", padx=30, pady=5)

        self.placeholder_pass = "Mật khẩu"
        pass_frame, self.entry_pass = self.create_entry_with_icon(
            login_frame, "🔒", self.placeholder_pass, show_char="*")
        pass_frame.pack(fill="x", padx=30, pady=5)

        self.show_pass_var = tk.BooleanVar(value=False)
        show_pass_check = tk.Checkbutton(
            pass_frame, text="👁️", font=self.font_normal,
            bg=self.BG_COLOR, activebackground=self.BG_COLOR,
            relief=tk.FLAT, bd=0, variable=self.show_pass_var,
            command=self.toggle_password_visibility)
        show_pass_check.pack(side="right", padx=(0, 5))

        login_button = tk.Button(login_frame, text="Đăng nhập",
                                 font=self.font_bold, bg=self.BTN_COLOR, fg="white",
                                 relief=tk.FLAT, bd=0,
                                 activebackground=self.BTN_ACTIVE,
                                 activeforeground="white",
                                 command=self.attempt_login)
        login_button.pack(fill="x", padx=30, pady=(30, 20), ipady=8)

    def create_entry_with_icon(self, parent, icon_text, placeholder, suffix_text=None, show_char=None):
        entry_frame = tk.Frame(parent, bg=self.BG_COLOR)
        line_frame = tk.Frame(entry_frame, bg=self.PLACEHOLDER_COLOR, height=1)
        line_frame.pack(side="bottom", fill="x")

        icon_label = tk.Label(entry_frame, text=icon_text,
                              font=self.font_normal,
                              bg=self.BG_COLOR,
                              fg=self.PLACEHOLDER_COLOR)
        icon_label.pack(side="left", padx=(0, 5))

        entry = tk.Entry(entry_frame,
                         font=self.font_normal,
                         fg=self.PLACEHOLDER_COLOR,
                         relief=tk.FLAT, bd=0,
                         show=show_char)
        entry.insert(0, placeholder)

        is_pass = (show_char == "*")
        entry.bind("<FocusIn>", partial(self.on_focus_in, entry, placeholder, icon_label, is_pass))
        entry.bind("<FocusOut>", partial(self.on_focus_out, entry, placeholder, icon_label, is_pass))

        if suffix_text:
            suffix_label = tk.Label(entry_frame, text=suffix_text,
                                    font=self.font_normal,
                                    bg=self.BG_COLOR,
                                    fg=self.PLACEHOLDER_COLOR)
            suffix_label.pack(side="right")

        entry.pack(side="left", fill="x", expand=True, ipady=5)
        return entry_frame, entry

    def on_focus_in(self, entry, placeholder, icon_label, is_password, event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=self.TEXT_COLOR)
            icon_label.config(fg=self.TEXT_COLOR)
            if is_password: entry.config(show="*")

    def on_focus_out(self, entry, placeholder, icon_label, is_password, event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=self.PLACEHOLDER_COLOR)
            icon_label.config(fg=self.PLACEHOLDER_COLOR)
            if is_password: entry.config(show="")

    def toggle_password_visibility(self):
        if self.show_pass_var.get():
            self.entry_pass.config(show="")
        else:
            if self.entry_pass.get() != self.placeholder_pass:
                self.entry_pass.config(show="*")

    def attempt_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        if (username == self.placeholder_user or
                password == self.placeholder_pass or
                not username or not password):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
            return
        (success, message, user) = self.auth_service.log_in(username, password)

        if success:
            from src.views.main_view import MainView
            self.destroy()
            try:
                app = MainView(current_user=user)
            except Exception as e:
                print(f"Lỗi khởi chạy MainView: {e}")
        else:
            messagebox.showerror("Lỗi đăng nhập", message)