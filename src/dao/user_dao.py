from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import User
from src.models.Enum import Status_user_Enum
from src.utils import hash_password


class UserDAO:
    def __init__(self):
        self.db = DatabaseConnection()

    def _convert_to_user_obj(self, row: dict) -> User:
        role_val = row['role']
        status_val = row['status_user']
        try:
            status_enum = Status_user_Enum(status_val)
        except ValueError:
            status_enum = status_val

        return User(
            user_id=row['user_id'],
            username=row['username'],
            password=row['password'],
            fullname=row['fullname'],
            role=role_val,
            status_user=status_enum,
            is_already_hashed=True
        )

    def add_user(self, user: User) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            r_val = user.role
            s_val = user.status_user.value if hasattr(user.status_user, 'value') else str(user.status_user)
            cursor.execute('''
                INSERT INTO user (username, password, fullname, role, status_user)
                VALUES (%s, %s, %s, %s, %s)
            ''', (user.username, user.password, user.fullname, r_val, s_val))
            conn.commit()
            user.user_id = cursor.lastrowid
            return True
        except Error as e:
            print(f"Lỗi thêm user: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()

    def update_user(self, user: User) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            r_val = user.role
            s_val = user.status_user.value if hasattr(user.status_user, 'value') else str(user.status_user)
            cursor.execute('''
                UPDATE user 
                SET fullname=%s, role=%s, status_user=%s
                WHERE user_id=%s
            ''', (user.fullname, r_val, s_val, user.user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi update user: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()

    def find_username(self, username: str) -> Optional[User]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user WHERE username=%s', (username,))
            row = cursor.fetchone()
            if row:
                return self._convert_to_user_obj(row)
            return None
        except Error as e:
            print(f"Lỗi find username: {e}")
            return None
        finally:
            if cursor: cursor.close()

    def find_userid(self, user_id: int) -> Optional[User]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user WHERE user_id=%s', (user_id,))
            row = cursor.fetchone()
            if row:
                return self._convert_to_user_obj(row)
            return None
        except Error as e:
            print(f"Lỗi find userid: {e}")
            return None
        finally:
            if cursor: cursor.close()

    def list_user(self) -> List[User]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user ORDER BY fullname')
            rows = cursor.fetchall()
            return [self._convert_to_user_obj(row) for row in rows]
        except Error as e:
            print(f"Lỗi list user: {e}")
            return []
        finally:
            if cursor: cursor.close()

    def change_password(self, user_id: int, new_password: str) -> bool:
        conn = None
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            hashed = hash_password(new_password)
            cursor.execute('UPDATE user SET password=%s WHERE user_id=%s', (hashed, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi đổi mật khẩu: {e}")
            if conn: conn.rollback()
            return False
        finally:
            if cursor: cursor.close()

    def find_fullname(self, fullname: str) -> Optional[User]:
        cursor = None
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user WHERE fullname=%s COLLATE utf8mb4_unicode_ci', (fullname,))
            row = cursor.fetchone()
            if row:
                return self._convert_to_user_obj(row)
            return None
        except Error as e:
            print(f"Lỗi tìm user theo tên: {e}")
            return None
        finally:
            if cursor: cursor.close()