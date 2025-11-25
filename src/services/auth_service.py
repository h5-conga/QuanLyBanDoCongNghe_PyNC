from typing import Optional
from src.dao.user_dao import UserDAO
from src.models.Enum import Status_user_Enum
from src.models.entity import User


class AuthService:
    def __init__(self):
        self.dao = UserDAO()
        self.current_user: Optional[User] = None

    def log_in(self, username: str, password: str) -> tuple[bool, str, Optional[User]]:
        user = self.dao.find_username(username)

        if not user:
            return False, "Tên đăng nhập không tồn tại", None

        if user.status_user != Status_user_Enum.ACTIVE:
            return False, "Tài khoản đã bị khóa", None

        if not user.check_password(password):
            return False, "Mật khẩu không đúng", None

        self.current_user = user
        return True, f"Đăng nhập thành công! Chào mừng {user.fullname}", user

    def log_out(self):
        self.current_user = None

    def check_admin_permission(self) -> bool:
        return self.current_user and self.current_user.check_admin()

    def get_user(self) -> Optional[User]:
        return self.current_user