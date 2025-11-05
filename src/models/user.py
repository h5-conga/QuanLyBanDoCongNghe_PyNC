class User:

    def __init__(self, user_id: str, username: str, password: str,
                 fullname: str, role: str,
                 status_user: str = "Active"):
        self.user_id = user_id
        self.username = username
        self.password = password  # Nên mã hóa trong thực tế
        self.fullname = fullname
        self.role = role  # admin, manager, cashier
        self.status_user = status_user  # active, loc

    def check_password(self, password: str) -> bool:
        return self.password == password

    def check_admin(self) -> bool:
        return self.role == "admin"

    def check_manager(self) -> bool:
        return self.role == "manager"

    def check_cashier(self) -> bool:
        return self.role == "cashier"

    def __str__(self):
        return f"User[{self.username}] {self.fullname} - {self.role}"