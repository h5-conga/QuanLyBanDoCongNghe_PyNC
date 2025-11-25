from typing import List
from src.dao.user_dao import UserDAO
from src.models.entity import User
from src.models.Enum import Role_Enum, Status_user_Enum
from src.services.auth_service import AuthService

class UserService:
    def __init__(self, auth_service: AuthService):
        self.dao = UserDAO()
        self.auth = auth_service

    def register_employee(self, username: str, password: str, fullname: str, role_str: str) -> tuple[bool, str]:
        if self.auth.current_user and not self.auth.check_admin_permission():
            return False, "Bạn không có quyền thêm tài khoản."
        valid_roles = [r.value for r in Role_Enum]
        if role_str not in valid_roles:
            return False, "Role không hợp lệ"
        if self.dao.find_username(username):
            return False, "Username đã tồn tại"
        new_user = User(
            user_id=None,
            username=username,
            password=password,
            fullname=fullname,
            role=role_str,
            status_user=Status_user_Enum.ACTIVE,
            is_already_hashed=False
        )

        if self.dao.add_user(new_user):
            return True, f"Tạo tài khoản {fullname} thành công"
        return False, "Lỗi khi lưu vào CSDL"

    def list_employees(self) -> List[User]:
        return self.dao.list_user()

    def toggle_user_status(self, user_id: int, current_operator_id: int = None) -> tuple[bool, str]:
        user = self.dao.find_userid(user_id)
        if not user:
            return False, "Không tìm thấy user."
        if current_operator_id is not None:
            try:
                if int(user.user_id) == int(current_operator_id):
                    return False, "Không thể khóa tài khoản bạn đang sử dụng để đăng nhập!"
            except ValueError:
                pass

        if user.status_user == Status_user_Enum.ACTIVE:
            user.status_user = Status_user_Enum.LOCK
            msg = "Đã KHÓA tài khoản."
        else:
            user.status_user = Status_user_Enum.ACTIVE
            msg = "Đã MỞ KHÓA tài khoản."

        if self.dao.update_user(user):
            return True, msg
        return False, "Lỗi cập nhật trạng thái."