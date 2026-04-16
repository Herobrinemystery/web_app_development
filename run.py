import os
import sqlite3
from flask import Flask
from dotenv import load_dotenv

from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.recipe_routes import recipe_bp

def create_app():
    load_dotenv()
    
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.secret_key = os.getenv('SECRET_KEY', 'default_dev_key_123')
    
    # 確保 instance 目錄與 database 目錄存在
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    # 註冊 Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
    
    return app

def init_db():
    """初始化資料庫與建立資料表"""
    db_path = os.path.join('instance', 'database.db')
    schema_path = os.path.join('database', 'schema.sql')
    
    os.makedirs('instance', exist_ok=True)
    
    if os.path.exists(schema_path):
        with sqlite3.connect(db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.commit()
        print("資料庫初始化完成！")
    else:
        print(f"錯誤：找不到 {schema_path}")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
