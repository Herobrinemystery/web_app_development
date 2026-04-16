from flask import Blueprint, request, render_template, redirect, url_for, flash, session

recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipe_bp.route('/my')
def my_recipes():
    """
    我的食譜專區。
    處理邏輯：驗證登入狀態，呼叫 Recipe.get_by_user(user_id)
    輸出：渲染 templates/recipes/my_recipes.html
    """
    pass

@recipe_bp.route('/new')
def new_recipe():
    """
    新增食譜頁面。
    輸出：渲染 templates/recipes/new.html
    """
    pass

@recipe_bp.route('/create', methods=['POST'])
def create_recipe():
    """
    建立食譜處理。
    輸入：title, steps, is_public, ingredients (可能有逗號或多個 input)
    處理邏輯：先解析食材並以 Ingredient.create() 或搜尋取得 IDs，再呼叫 Recipe.create()
    輸出：重導向 /recipes/my 或新食譜的詳情頁
    """
    pass

@recipe_bp.route('/<int:recipe_id>')
def detail(recipe_id):
    """
    食譜詳細閱讀頁面。
    輸入：recipe_id
    處理邏輯：呼叫 Recipe.get_by_id(recipe_id) (須包含食材清單)
    輸出：渲染 templates/recipes/detail.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    """
    編輯食譜頁面。
    處理邏輯：驗證是否為作者後，載入內容並渲染 templates/recipes/edit.html
    """
    pass

@recipe_bp.route('/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    """
    更新食譜。
    輸入：修改後的 title, steps, is_public 等
    處理邏輯：驗證權限，重新解析食材清單，呼叫 Recipe.update()
    輸出：重導向回詳情頁
    """
    pass

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜。
    處理邏輯：驗證權限後呼叫 Recipe.delete()
    輸出：重導向 /recipes/my 或首頁
    """
    pass

@recipe_bp.route('/search')
def search():
    """
    尋找可以做的食譜 (核心功能：依據目前所擁有的食材查找食譜)
    輸入：Query String (例如 ?q=高麗菜,豬肉)
    處理邏輯：依賴 Ingredient.search_by_name 找出對應食材 IDs 後交給 Recipe.search_by_ingredients
    輸出：回傳搜尋結果並渲染 templates/recipes/search.html
    """
    pass
