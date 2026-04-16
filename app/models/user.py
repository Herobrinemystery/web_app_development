import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class User:
    @staticmethod
    def create(username, password_hash, role='user'):
        """建立新使用者"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                (username, password_hash, role)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None # Username already exists
        except Exception as e:
            print(f"Error creating user: {e}")
            return None

    @staticmethod
    def get_by_id(user_id):
        """用 ID 取得單一使用者"""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_username(username):
        """用帳號取得使用者 (用於登入)"""
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        return user

    @staticmethod
    def get_all():
        """取得所有使用者列表 (管理員功能)"""
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        return users

    @staticmethod
    def update(user_id, data):
        """更新使用者資料"""
        try:
            conn = get_db_connection()
            # 依據傳入的 data 組合 SQL (例如更新 role 或是 password_hash)
            fields = []
            values = []
            for k, v in data.items():
                fields.append(f"{k} = ?")
                values.append(v)
            
            if not fields:
                return False
                
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            
            conn.execute(query, tuple(values))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """刪除使用者"""
        try:
            conn = get_db_connection()
            conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

