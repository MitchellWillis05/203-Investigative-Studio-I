# import sqlite3 for database interaction
import sqlite3


# database connection method
def db_connect():
    conn = None
    try:
        conn = sqlite3.connect("user_database.db")
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
    return conn


def create_new_entry(userid, title, mood, color, content, date):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO journal (userid, title, mood, color, content, date) VALUES (?, ?, ?, ?, ?, ?)",
                    (userid, title, mood, color, content, date)
                    )
        conn.commit()
        print('done')
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False
    finally:
        cur.close()
        conn.close()


def fetch_entry_by_entryid(entryid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT userid, title, mood, color, content, date FROM journal WHERE entryid = ?",
                    (entryid,))
        data_fetched = cur.fetchall()
        return data_fetched[0]
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None
    except IndexError as error:
        print("error fetching entry by entry id")
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def fetch_entries_by_userid(userid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT entryid, userid, title, mood, color, content, date FROM journal WHERE userid = ?",
                    (userid,))
        data_fetched = cur.fetchall()
        return data_fetched
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    except IndexError as error:
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def delete_entry_by_entryid(entryid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM journal WHERE entryid = ?", (entryid,))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False

    except IndexError as error:
        print(error)
        return False
    finally:
        cur.close()
        conn.close()


def check_generation_vacancy(entryid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT generated_response FROM journal WHERE entryid = ?", (entryid,))
        fetched = cur.fetchall()
        return fetched[0][0]
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    except IndexError as error:
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def enter_generation_into_entry(ai_prompt, entryid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE journal SET generated_response = ? WHERE entryid = ?", (ai_prompt, entryid))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False

    except IndexError as error:
        print(error)
        return False
    finally:
        cur.close()
        conn.close()


def truncate_string(s, length):
    if len(s) > length:
        return s[:length] + "..."
    return s


def get_journal_preview(data):
    modified_data = []

    for row in data:
        row_list = list(row)
        row_list[5] = truncate_string(row_list[5], 35)
        modified_row = tuple(row_list)
        modified_data.append(modified_row)

    return modified_data
