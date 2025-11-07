from src.models.Enum import Role_Enum, Status_user_Enum
from src.utils import hash_password, check_password


class User:

    def __init__(self, user_id: int, username: str, password: str,
                 fullname: str, role: Role_Enum,
                 status_user: Status_user_Enum = Status_user_Enum.ACTIVE):
        self.user_id = user_id
        self.username = username
        self.password = hash_password(password)
        self.fullname = fullname
        self.role = role  # admin, manager, cashier
        self.status_user = status_user  # active, lock

    def check_password(self, password: str) -> bool:
        return check_password(password, self.password)

    def check_admin(self) -> bool:
        return self.role == "admin"

    def check_manager(self) -> bool:
        return self.role == "manager"

    def check_cashier(self) -> bool:
        return self.role == "cashier"

    def __str__(self):
        return f"User[{self.username}] {self.fullname} - {self.role}"