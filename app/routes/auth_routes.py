from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理註冊。
    GET: 顯示註冊表單 (templates/auth/register.html)
    POST: 接收表單並呼叫 User.create()。成功則導向 login()。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('請輸入帳號和密碼', 'error')
            return redirect(url_for('auth.register'))
            
        password_hash = generate_password_hash(password)
        user_id = User.create(username, password_hash)
        
        if user_id:
            flash('註冊成功！麻煩再次登入', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('此帳號可能已被使用或發生錯誤', 'error')
            return redirect(url_for('auth.register'))
            
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理登入。
    GET: 顯示登入表單 (templates/auth/login.html)
    POST: 接收表單並呼叫 User.get_by_username() 驗證。成功則設定 session 並導向首頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('登入成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('帳號或密碼錯誤', 'error')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """
    登出處理。
    清除 session 並導回首頁。
    """
    session.clear()
    flash('您已經登出', 'info')
    return redirect(url_for('main.index'))
