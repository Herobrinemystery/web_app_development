from flask import Blueprint, request, render_template, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    註冊頁面與處理註冊。
    GET: 顯示註冊表單 (templates/auth/register.html)
    POST: 接收表單並呼叫 User.create()。成功則導向 login()。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登入頁面與處理登入。
    GET: 顯示登入表單 (templates/auth/login.html)
    POST: 接收表單並呼叫 User.get_by_username() 驗證。成功則設定 session 並導向首頁。
    """
    pass

@auth_bp.route('/logout')
def logout():
    """
    登出處理。
    清除 session 並導回首頁。
    """
    pass
