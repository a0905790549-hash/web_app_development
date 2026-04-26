import os
from flask import Flask

def create_app():
    """建立並初始化 Flask Application"""
    app = Flask(__name__)
    
    # 讀取設定或是設定基礎的 secret_key (為了 flash message 需要)
    app.secret_key = 'dev_secret_key'  # 實務上請改用環境變數

    # 在此處註冊 Blueprints
    from app.routes.draw_routes import draw_bp
    app.register_blueprint(draw_bp)

    return app
