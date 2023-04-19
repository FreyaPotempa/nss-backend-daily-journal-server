import sqlite3
from models import Entry, Mood


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
                e.mood_id,
                m.id,
                m.mood
            FROM JournalEntries e
            JOIN Moods m
                ON m.id = e.mood_id
            ''')

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            entry = Entry(row["id"], row["concept"],
                          row["entry"], row["mood_id"])

            mood = Mood(row["id"], row["mood"])

            entry.mood = mood.__dict__

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


def get_searched_entries(search_term):
    '''get single entry by search term'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
            SELECT id, concept, entry, mood_id
            FROM JournalEntries
            WHERE entry LIKE ?
            ''', ('%' + search_term + '%', ))

        entries = []

        dataset = db_cursor.fetchall()

        if dataset:
            for data in dataset:
                entry = Entry(data["id"], data["concept"],
                              data["entry"], data["mood_id"])

                entries.append(entry.__dict__)
        return entries


def delete_entry(id):
    '''delete a single entry'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute('''
            DELETE FROM JournalEntries
            WHERE id = ?
            ''', (id, ))


def update_entry(id, new_entry):
    '''updates an entry'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
            UPDATE JournalEntries
                SET
                concept = ?,
                entry = ?,
                mood_id = ?
            WHERE id = ?
            ''', (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True


def create_entry(new_entry):
    '''create a new journal entry'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute('''
        INSERT INTO JournalEntries
            ( concept, entry, mood_id)
        VALUES
            (?,?,?);
            ''', (new_entry['concept'], new_entry['entry'], new_entry['mood_id']))

        id = db_cursor.lastrowid

        new_entry["id"] = id

    return new_entry
