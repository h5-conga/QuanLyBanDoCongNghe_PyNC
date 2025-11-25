from src.services.auth_service import AuthService
from src.services.user_service import UserService
from src.views.login_view import LoginView


def main():
    try:
        auth_service = AuthService()
        user_service = UserService(auth_service)
    except Exception as e:
        print(f"Lỗi kết nối Database hoặc Service: {e}")
        return
    app = LoginView(auth_service=auth_service, user_service=user_service)
    app.mainloop()


if __name__ == "__main__":
    main()