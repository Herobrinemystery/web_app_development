from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    首頁：顯示最新公開的食譜。
    處理邏輯：呼叫 Recipe.get_all(public_only=True)
    輸出：渲染 templates/index.html
    """
    pass
