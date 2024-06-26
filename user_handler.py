# import sqlite3 for database interaction
import sqlite3
import password_handler as ph
from datetime import datetime, timedelta


# database connection method
def db_connect():
    conn = None
    try:
        conn = sqlite3.connect("user_database.db")
    except sqlite3.Error as error:
        print(error.sqlite_errorcode)
        print(error.sqlite_errorname)
    return conn


def check_unique_cred(username, email):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        results_u = cur.fetchall()
        cur.execute("SELECT * FROM user WHERE email = ?", (email.lower(),))
        results_e = cur.fetchall()
        if len(results_u) == 0:
            if len(results_e) == 0:
                return 2
            else:
                return 1
        else:
            return 0
    finally:
        cur.close()
        conn.close()


def check_username(username):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        results = cur.fetchall()
        if len(results) == 0:
            return True  # username does not exist in database
        else:
            return False  # user exists in database
    finally:
        cur.close()
        conn.close()


def check_email(email):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM user WHERE email = ?", (email.lower(),))
        results = cur.fetchall()
        if len(results) == 0:
            return True  # email does not exist in database
        else:
            return False  # email exists in database
    finally:
        cur.close()
        conn.close()


def create_new_user(username, email, password, day, month, year, starsign, gender):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO user (username, email, password, dob_day, dob_month, dob_year, starsign, gender, last_request) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (username, email.lower(), password, int(day), int(month), int(year), starsign, gender, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False
    finally:
        cur.close()
        conn.close()


def update_password(user_id, new_password):
    conn = db_connect()
    cur = conn.cursor()
    try:
        new_password = ph.encrypt_password(new_password)
        cur.execute("UPDATE user SET password = ? WHERE userid = ?", (new_password, user_id))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False
    finally:
        cur.close()
        conn.close()


def validate_login(email, password):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT password FROM user WHERE email = ?", (email.lower(),))
        password_fetched = cur.fetchall()
        if ph.verify_password(password, password_fetched[0][0]):
            return True
        else:
            return False
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False
    except IndexError as error:
        print("error validating login")
        print(error)
        return False
    finally:
        cur.close()
        conn.close()


def fetch_user_by_email(email):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT userid FROM user WHERE email = ?", (email.lower(),))
        user_fetched = cur.fetchall()
        return user_fetched[0][0]
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None
    except IndexError as error:
        print("error fetching user by email")
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def fetch_prompt_info_by_userid(userid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT starsign, gender FROM user WHERE userid = ?", (userid,))
        data_fetched = cur.fetchall()
        return data_fetched[0]
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    except IndexError as error:
        print("error fetching prompt info")
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def fetch_last_request(userid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT last_request FROM user WHERE userid = ?", (userid,))
        data_fetched = cur.fetchall()
        return data_fetched[0][0]
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    except IndexError as error:
        print("error fetching last request")
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def fetch_cred_by_id(userid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, email,"
                    " dob_day, dob_month,"
                    " dob_year, starsign,"
                    " gender FROM user WHERE userid = ?", (userid,))
        data_fetched = cur.fetchall()
        return data_fetched[0]
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return None

    except IndexError as error:
        print("error fetching credentials by id")
        print(error)
        return None
    finally:
        cur.close()
        conn.close()


def new_request(userid):
    conn = db_connect()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE user SET last_request = ? WHERE userid = ?",
                    (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), userid))
        conn.commit()
        return True
    except sqlite3.Error as error:
        print(f"SQLite error: {error}")
        return False
    finally:
        cur.close()
        conn.close()
