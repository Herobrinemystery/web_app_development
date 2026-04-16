from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient

recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

def handle_ingredients_string(ingredients_str):
    """將逗號分隔的食材字串轉換成對應的 Ingredient ID 清單"""
    if not ingredients_str:
        return []
    
    ingredient_ids = []
    # 以逗號分隔，去掉前後空白
    names = [name.strip() for name in ingredients_str.split(',') if name.strip()]
    for name in names:
        ing_id = Ingredient.create(name)
        if ing_id:
            ingredient_ids.append(ing_id)
    return ingredient_ids

@recipe_bp.route('/my')
def my_recipes():
    """我的食譜專區"""
    if 'user_id' not in session:
        flash('請先登入', 'error')
        return redirect(url_for('auth.login'))
        
    recipes = Recipe.get_by_user(session['user_id'])
    return render_template('recipes/my_recipes.html', recipes=recipes)

@recipe_bp.route('/new')
def new_recipe():
    """新增食譜頁面"""
    if 'user_id' not in session:
        flash('請先登入', 'error')
        return redirect(url_for('auth.login'))
    return render_template('recipes/new.html')

@recipe_bp.route('/create', methods=['POST'])
def create_recipe():
    """建立食譜處理"""
    if 'user_id' not in session:
        flash('請先登入', 'error')
        return redirect(url_for('auth.login'))
        
    title = request.form.get('title')
    steps = request.form.get('steps')
    is_public = request.form.get('is_public') == 'on'
    ingredients_str = request.form.get('ingredients', '')
    
    if not title or not steps:
        flash('標題與步驟為必填', 'error')
        return redirect(url_for('recipes.new_recipe'))
        
    ingredient_ids = handle_ingredients_string(ingredients_str)
    
    recipe_id = Recipe.create(session['user_id'], title, steps, is_public, ingredient_ids)
    if recipe_id:
        flash('成功建立食譜！', 'success')
        return redirect(url_for('recipes.detail', recipe_id=recipe_id))
    else:
        flash('建立食譜時發生錯誤', 'error')
        return redirect(url_for('recipes.new_recipe'))

@recipe_bp.route('/<int:recipe_id>')
def detail(recipe_id):
    """食譜詳細閱讀頁面"""
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        flash('找不到該食譜', 'error')
        return redirect(url_for('main.index'))
        
    # 如果是私有食譜，只有作者能看
    if not recipe['is_public']:
        if 'user_id' not in session or session['user_id'] != recipe['user_id']:
            flash('您沒有權限觀看這份食譜', 'error')
            return redirect(url_for('main.index'))
            
    return render_template('recipes/detail.html', recipe=recipe)

@recipe_bp.route('/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    """編輯食譜頁面"""
    if 'user_id' not in session:
        flash('請先登入', 'error')
        return redirect(url_for('auth.login'))
        
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('您沒有權限編輯此食譜', 'error')
        return redirect(url_for('recipes.my_recipes'))
        
    # 將食材清單組成逗號字串供前端顯示
    ing_str = ', '.join([ing['name'] for ing in recipe['ingredients']])
    
    return render_template('recipes/edit.html', recipe=recipe, ingredients_str=ing_str)

@recipe_bp.route('/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    """更新食譜"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('您沒有權限編輯此食譜', 'error')
        return redirect(url_for('recipes.my_recipes'))
        
    title = request.form.get('title')
    steps = request.form.get('steps')
    is_public = request.form.get('is_public') == 'on'
    ingredients_str = request.form.get('ingredients', '')
    
    ingredient_ids = handle_ingredients_string(ingredients_str)
    
    success = Recipe.update(recipe_id, title, steps, is_public, ingredient_ids)
    if success:
        flash('食譜更新成功！', 'success')
        return redirect(url_for('recipes.detail', recipe_id=recipe_id))
    else:
        flash('更新發生錯誤', 'error')
        return redirect(url_for('recipes.edit_recipe', recipe_id=recipe_id))

@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """刪除食譜"""
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe or recipe['user_id'] != session['user_id']:
        flash('無權刪除', 'error')
        return redirect(url_for('recipes.my_recipes'))
        
    Recipe.delete(recipe_id)
    flash('食譜已刪除', 'success')
    return redirect(url_for('recipes.my_recipes'))

@recipe_bp.route('/search')
def search():
    """尋找可以做的食譜"""
    q = request.args.get('q', '').strip()
    if not q:
        return render_template('recipes/search.html', query='', recipes=[])
        
    ingredient_names = [name.strip() for name in q.split(',') if name.strip()]
    ingredient_ids = []
    
    for name in ingredient_names:
        ings = Ingredient.search_by_name(name)
        for ing in ings:
            if ing['id'] not in ingredient_ids:
                ingredient_ids.append(ing['id'])
                
    if not ingredient_ids:
         # 找不到這些食材
         return render_template('recipes/search.html', query=q, recipes=[])
         
    recipes = Recipe.search_by_ingredients(ingredient_ids)
    return render_template('recipes/search.html', query=q, recipes=recipes)
