from typing import Optional, List
from mysql.connector import Error
from src.config import DatabaseConnection
from src.models.entity import User
from src.utils import hash_password


class UserDAO:
    """Data Access Object cho bảng user"""

    def __init__(self):
        self.db = DatabaseConnection()

    def add_user(self, user: User) -> bool:
        """Thêm user mới (user_id tự tăng)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user (username, password, fullname, role, status_user)
                VALUES (%s, %s, %s, %s, %s)
            ''', (
                user.username, user.password, user.fullname,
                user.role, user.status_user
            ))
            conn.commit()
            user.ma_user = cursor.lastrowid
            return True
        except Error as e:
            print(f"Lỗi khi thêm user: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def update_user(self, user: User) -> bool:
        """Cập nhật thông tin user"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user 
                SET fullname=%s, role=%s, status_user=%s
                WHERE user_id=%s
            ''', (user.fullname, user.role, user.status_user, user.user_id))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi cập nhật user: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def change_password(self, user_id: int, new_password: str) -> bool:
        """Đổi mật khẩu (hash trước khi lưu)"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            # Hash mật khẩu mới trước khi lưu
            hashed = hash_password(new_password)
            cursor.execute(
                'UPDATE user SET password=%s WHERE user_id=%s',
                (hashed, user_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Lỗi khi đổi mật khẩu: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()

    def find_username(self, username: str) -> Optional[User]:
        """Tìm user theo username"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user WHERE username=%s', (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row['user_id'], username=row['username'], password=row['password'],
                    fullname=row['fullname'], role=row['role'], status_user=row['status_user']
                )
            return None
        except Error as e:
            print(f"Lỗi khi tìm user theo username: {e}")
            return None
        finally:
            cursor.close()

    def find_userid(self, user_id: int) -> Optional[User]:
        """Tìm user theo user_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user WHERE user_id=%s', (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row['user_id'], username=row['username'], password=row['password'],
                    fullname=row['fullname'], role=row['role'], status_user=row['status_user']
                )
            return None
        except Error as e:
            print(f"Lỗi khi tìm user theo ID: {e}")
            return None
        finally:
            cursor.close()

    def find_fullname(self, fullname: str) -> Optional[User]:
        """Tìm user theo user_id"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user WHERE fullname=%s COLLATE utf8mb4_unicode_ci', (fullname,))
            row = cursor.fetchone()
            if row:
                return User(
                    user_id=row['user_id'], username=row['username'], password=row['password'],
                    fullname=row['fullname'], role=row['role'], status_user=row['status_user']
                )
            return None
        except Error as e:
            print(f"Lỗi khi tìm user theo họ tên: {e}")
            return None
        finally:
            cursor.close()

    def list_user(self) -> List[User]:
        """Lấy tất cả user"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM user ORDER BY fullname')
            rows = cursor.fetchall()
            return [
                User(
                    user_id=row['user_id'], username=row['username'], password=row['password'],
                    fullname=row['fullname'], role=row['role'], status_user=row['status_user']
                )
                for row in rows
            ]
        except Error as e:
            print(f"Lỗi khi lấy danh sách user: {e}")
            return []
        finally:
            cursor.close()
