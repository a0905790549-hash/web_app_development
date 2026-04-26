from flask import Blueprint, render_template, request, redirect, url_for, flash

# 建立名為 draw_routes 的 Blueprint
draw_bp = Blueprint('draw', __name__)

@draw_bp.route('/', methods=['GET'])
def index():
    """
    對應 `GET /`
    顯示首頁，包含填寫活動資訊、抽出數量與參加者名單的表單。
    """
    pass

@draw_bp.route('/draw', methods=['POST'])
def draw():
    """
    對應 `POST /draw`
    接收首頁表單送出的資料。
    進行資料驗證，若無誤則執行隨機抽籤，
    將結果存入資料庫後，重導向至 /results/<id>。
    """
    pass

@draw_bp.route('/results', methods=['GET'])
def list_results():
    """
    對應 `GET /results`
    取得所有歷史抽籤活動的列表，並渲染到歷史紀錄頁面。
    """
    pass

@draw_bp.route('/results/<int:id>', methods=['GET'])
def show_result(id):
    """
    對應 `GET /results/<id>`
    取得特定 ID 的抽籤活動結果與參與者名單。
    若帶有特定的 query parameter (例如 play_anim=1)，可觸發前端的抽籤動畫。
    """
    pass
