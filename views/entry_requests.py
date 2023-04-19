import sqlite3
from models import Entry


def get_all_entries():
    '''function that returns all entries'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
            SELECT
                e.id,
                e.concept,
                e.entry,
                e.mood_id
            FROM JournalEntries e
            ''')

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entry(row["id"], row["concept"],
                          row["entry"], row["mood_id"])

            entries.append(entry.__dict__)

    return entries


def get_single_entry(id):
    '''get single entry by id'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
            SELECT
                e.id,
                e.concept,
                e.entry,
                e.mood_id
            FROM JournalEntries e
            WHERE e.id = ?
            ''', (id, ))

        data = db_cursor.fetchone()

        entry = Entry(data["id"], data["concept"],
                      data["entry"], data["mood_id"])

        return entry.__dict__


def get_searched_entry(search_term):
    '''get single entry by search term'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
            SELECT * FROM JournalEntries
            WHERE `entry` LIKE ?
            ''', (search_term, ))

        data = db_cursor.fetchone()

        entry = Entry(data["id"], data["concept"],
                      data["entry"], data["mood_id"])

        return entry.__dict__


def delete_entry(id):
    '''delete a single entry'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute('''
            DELETE FROM JournalEntries
            WHERE id = ?
            ''', (id, ))
