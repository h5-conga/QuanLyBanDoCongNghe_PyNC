import tkinter as tk
from tkinter import messagebox

def handle_open_account(controller, main_controller=None):
    if main_controller and hasattr(main_controller, 'switch_view'):
        main_controller.switch_view("Tài khoản")
    else:
        try:
            from src.views.account_view import AccountView
            top = tk.Toplevel()
            top.title("Quản lý tài khoản")
            top.geometry("900x600")

            app = AccountView(master=top)
            app.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở giao diện tài khoản: {e}")

def handle_logout(view_instance):
    if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất không?"):
        if hasattr(view_instance, 'main_controller') and view_instance.main_controller:
            view_instance.main_controller.destroy()
        else:
            try:
                view_instance.winfo_toplevel().destroy()
            except Exception:
                pass
        try:
            from src.services.auth_service import AuthService
            from src.services.user_service import UserService
            from src.views.login_view import LoginView
            auth_service = AuthService()
            user_service = UserService(auth_service)
            login_app = LoginView(auth_service=auth_service, user_service=user_service)
            login_app.mainloop()

        except Exception as e:
            print(f"Lỗi khi mở lại màn hình đăng nhập: {e}")
            messagebox.showerror("Lỗi", f"Không thể mở lại màn hình đăng nhập.\nChi tiết: {e}")


def handle_check_inventory(master=None, threshold=10):
    """
    Logic kiểm tra tồn kho và gọi View hiển thị
    """
    try:
        from src.services.product_service import ProductService
        from src.views.stock_check_view import StockCheckView

        service = ProductService()
        # Hàm này trả về List[Product] (Object)
        low_stock_items = service.get_low_stock(threshold)

        out_of_stock = []  # Hết hàng
        near_out_of_stock = []  # Sắp hết

        for p in low_stock_items:
            # --- SỬA LỖI TẠI ĐÂY ---
            # Truy cập trực tiếp thuộc tính stock_quantity của object Product
            if p.stock_quantity <= 0:
                out_of_stock.append(p)
            else:
                near_out_of_stock.append(p)

        if not out_of_stock and not near_out_of_stock:
            messagebox.showinfo("Thông báo", f"Kho hàng ổn định.\nKhông có sản phẩm nào dưới định mức ({threshold}).")
            return

        # Gọi View
        StockCheckView(master, out_of_stock, near_out_of_stock)

    except Exception as e:
        # In chi tiết lỗi ra console để dễ debug nếu còn lỗi
        print(f"DEBUG ERROR: {e}")
        messagebox.showerror("Lỗi", f"Không thể kiểm tra tồn kho: {e}")