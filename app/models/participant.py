from app.models.database import get_db_connection

class Participant:
    @staticmethod
    def create_many(event_id, participants_data):
        """
        批次建立參加者紀錄
        :param participants_data: 包含 dict 的 list, 例如 [{"name": "A", "is_winner": 1}, ...]
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 準備批次插入的資料格式
        records = [(event_id, p['name'], p.get('is_winner', 0)) for p in participants_data]
        
        cursor.executemany(
            'INSERT INTO participants (event_id, name, is_winner) VALUES (?, ?, ?)',
            records
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_event_id(event_id):
        """取得特定活動的所有參加者名單"""
        conn = get_db_connection()
        participants = conn.execute('SELECT * FROM participants WHERE event_id = ?', (event_id,)).fetchall()
        conn.close()
        return participants

    @staticmethod
    def get_winners_by_event_id(event_id):
        """取得特定活動中所有「中籤」的參加者名單"""
        conn = get_db_connection()
        winners = conn.execute('SELECT * FROM participants WHERE event_id = ? AND is_winner = 1', (event_id,)).fetchall()
        conn.close()
        return winners
