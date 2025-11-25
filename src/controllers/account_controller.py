from src.services.user_service import UserService
from src.services.auth_service import AuthService


class AccountController:
    def __init__(self):
        self.auth_service = AuthService()
        self.user_service = UserService(self.auth_service)

    def get_all_users_view(self):
        users = self.user_service.list_employees()
        data = []
        for u in users:
            r_val = u.role.value if hasattr(u.role, 'value') else str(u.role)

            s_val = u.status_user.value if hasattr(u.status_user, 'value') else str(u.status_user)

            data.append({
                "id": u.user_id,
                "username": u.username,
                "fullname": u.fullname,
                "role": r_val,
                "status": s_val
            })
        return data

    def add_new_user(self, username, password, fullname, role, status):
        if not username or not password or not fullname:
            return False, "Vui lòng nhập đủ thông tin."
        return self.user_service.register_employee(username, password, fullname, role)

    def toggle_status(self, user_id, current_user_id=None):
        return self.user_service.toggle_user_status(user_id, current_operator_id=current_user_id)