from src.models.Enum import Role_Enum, Status_user_Enum
from src.utils import hash_password, check_password

class User:

    def __init__(self, user_id: int, username: str, password: str,
                 fullname: str, role: Role_Enum,
                 status_user: Status_user_Enum = Status_user_Enum.ACTIVE,
                 is_already_hashed: bool = False):
        self.user_id = user_id
        self.username = username
        self.fullname = fullname
        self.role = role
        self.status_user = status_user
        if is_already_hashed:
            self.password = password
        else:
            self.password = hash_password(password)

    def check_password(self, password_input: str) -> bool:
        return check_password(password_input, self.password)

    def check_admin(self) -> bool:
        return self.role == "admin"

    def check_cashier(self) -> bool:
        return self.role == "cashier"
