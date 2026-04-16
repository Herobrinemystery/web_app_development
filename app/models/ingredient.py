import sqlite3

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Ingredient:
    @staticmethod
    def create(name):
        """建立新食材 (如果不存在則新增)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO ingredients (name) VALUES (?)', (name,))
            conn.commit()
            
            # 取得食材的 ID (無論是剛剛新增還是已經存在的)
            ingredient = cursor.execute('SELECT id FROM ingredients WHERE name = ?', (name,)).fetchone()
            conn.close()
            return ingredient['id'] if ingredient else None
        except Exception as e:
            print(f"Error creating ingredient: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有食材"""
        conn = get_db_connection()
        ingredients = conn.execute('SELECT * FROM ingredients').fetchall()
        conn.close()
        return ingredients

    @staticmethod
    def get_by_id(ingredient_id):
        """用 ID 取得食材"""
        conn = get_db_connection()
        ingredient = conn.execute('SELECT * FROM ingredients WHERE id = ?', (ingredient_id,)).fetchone()
        conn.close()
        return ingredient

    @staticmethod
    def search_by_name(keyword):
        """用名稱搜尋食材"""
        conn = get_db_connection()
        ingredients = conn.execute('SELECT * FROM ingredients WHERE name LIKE ?', (f'%{keyword}%',)).fetchall()
        conn.close()
        return ingredients
