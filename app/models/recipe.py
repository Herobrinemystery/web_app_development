import sqlite3
import datetime

def get_db_connection():
    conn = sqlite3.connect('instance/database.db')
    conn.row_factory = sqlite3.Row
    return conn

class Recipe:
    @staticmethod
    def create(user_id, title, steps, is_public=False, ingredient_ids=None):
        """建立新食譜，並關聯食材"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                'INSERT INTO recipes (user_id, title, steps, is_public, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)',
                (user_id, title, steps, is_public, now, now)
            )
            recipe_id = cursor.lastrowid
            
            # 如果有提供食材 ID 列表，則寫入關聯表
            if ingredient_ids:
                for ing_id in ingredient_ids:
                    cursor.execute(
                        'INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)',
                        (recipe_id, ing_id)
                    )
            
            conn.commit()
            conn.close()
            return recipe_id
        except Exception as e:
            print(f"Error creating recipe: {e}")
            return None

    @staticmethod
    def get_all(public_only=True):
        """取得所有食譜"""
        conn = get_db_connection()
        query = 'SELECT * FROM recipes'
        if public_only:
            query += ' WHERE is_public = 1'
        query += ' ORDER BY created_at DESC'
        recipes = conn.execute(query).fetchall()
        conn.close()
        return recipes

    @staticmethod
    def get_by_user(user_id):
        """取得某使用者的所有食譜"""
        conn = get_db_connection()
        recipes = conn.execute('SELECT * FROM recipes WHERE user_id = ? ORDER BY created_at DESC', (user_id,)).fetchall()
        conn.close()
        return recipes

    @staticmethod
    def get_by_id(recipe_id):
        """用 ID 取得單一食譜，包含關聯的食材"""
        conn = get_db_connection()
        recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (recipe_id,)).fetchone()
        
        ingredients = []
        if recipe:
            ings = conn.execute('''
                SELECT i.id, i.name 
                FROM ingredients i
                JOIN recipe_ingredients ri ON i.id = ri.ingredient_id
                WHERE ri.recipe_id = ?
            ''', (recipe_id,)).fetchall()
            ingredients = [dict(i) for i in ings]
            
        conn.close()
        
        # 轉成 dict 將即時食材加入
        if recipe:
            recipe_dict = dict(recipe)
            recipe_dict['ingredients'] = ingredients
            return recipe_dict
        return None

    @staticmethod
    def update(recipe_id, title, steps, is_public, ingredient_ids=None):
        """更新食譜資訊"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute(
                'UPDATE recipes SET title = ?, steps = ?, is_public = ?, updated_at = ? WHERE id = ?',
                (title, steps, is_public, now, recipe_id)
            )
            
            if ingredient_ids is not None:
                # 重新設定食材關聯：先刪除舊關聯再新增
                cursor.execute('DELETE FROM recipe_ingredients WHERE recipe_id = ?', (recipe_id,))
                for ing_id in ingredient_ids:
                    cursor.execute(
                        'INSERT INTO recipe_ingredients (recipe_id, ingredient_id) VALUES (?, ?)',
                        (recipe_id, ing_id)
                    )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating recipe: {e}")
            return False

    @staticmethod
    def delete(recipe_id):
        """刪除食譜"""
        conn = get_db_connection()
        # 自動開啟 foreign key constraint 刪除連動項目 (需看 sqlite 設定)
        # SQLite 的 ON DELETE CASCADE 需在連線時執行 PRAGMA foreign_keys = ON;
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()
        return True
        
    @staticmethod
    def search_by_ingredients(ingredient_ids):
        """核心 MVP 功能：輸入多個食材 ID，尋找包含這些食材的食譜 (只要包含其中之一即可，可依配對數排序)"""
        # 注意此為簡易版實作，可針對複雜應用再調整
        if not ingredient_ids:
            return []
            
        conn = get_db_connection()
        placeholders = ','.join('?' * len(ingredient_ids))
        
        # 複雜查詢：先找出有包含指定食材的 recipe，並計算命中幾樣食材
        query = f'''
            SELECT r.*, COUNT(ri.ingredient_id) as match_count
            FROM recipes r
            JOIN recipe_ingredients ri ON r.id = ri.recipe_id
            WHERE ri.ingredient_id IN ({placeholders}) AND r.is_public = 1
            GROUP BY r.id
            ORDER BY match_count DESC, r.created_at DESC
        '''
        
        recipes = conn.execute(query, tuple(ingredient_ids)).fetchall()
        conn.close()
        return recipes
