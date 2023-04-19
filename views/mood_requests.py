import sqlite3
from models import Mood


def get_all_moods():
    '''function that returns all moods'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
            SELECT
                m.id,
                m.mood
            FROM Moods m
            ''')

        moods = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            mood = Mood(row["id"], row["mood"])

            moods.append(mood.__dict__)
    return moods
