import sqlite3
import os

# 資料庫檔案的路徑
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'app.db')

def get_db_connection():
    """取得 SQLite 資料庫連線"""
    # 確保 instance 資料夾存在
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    # 將回傳結果轉換為 dict-like 的 Row 物件
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫與資料表"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            
        conn = get_db_connection()
        conn.executescript(schema_sql)
        conn.commit()
        conn.close()
