from app.models.database import get_db_connection

class Event:
    @staticmethod
    def create(title, draw_count):
        """建立一筆新的抽籤活動紀錄，並回傳其 id"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO events (title, draw_count) VALUES (?, ?)',
            (title, draw_count)
        )
        conn.commit()
        event_id = cursor.lastrowid
        conn.close()
        return event_id

    @staticmethod
    def get_by_id(event_id):
        """透過 id 取得單一活動紀錄"""
        conn = get_db_connection()
        event = conn.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
        conn.close()
        return event

    @staticmethod
    def get_all():
        """取得所有活動紀錄，以建立時間倒序排列"""
        conn = get_db_connection()
        events = conn.execute('SELECT * FROM events ORDER BY created_at DESC').fetchall()
        conn.close()
        return events

    @staticmethod
    def delete(event_id):
        """刪除指定的活動紀錄"""
        conn = get_db_connection()
        # 由於開啟了 CASCADE（若有支援），可能也會連帶刪除 participants，
        # 但為求保險通常 sqlite3 需要先執行 PRAGMA foreign_keys = ON
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('DELETE FROM events WHERE id = ?', (event_id,))
        conn.commit()
        conn.close()
