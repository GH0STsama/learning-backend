import sqlite3
from user import User
from threading import Lock

# database write lock
lock = Lock()

db = sqlite3.connect("./database/database.db", check_same_thread = False)
cursor = db.cursor()


def create_user(user: User) -> User | None:
    """Insert a new user into users table"""

    sql_keys = []; parameters = []
    for element in user.__dict__.items():
        sql_keys.append(element[0])
        parameters.append(element[1])

    sql_values = "?, " * len(parameters)

    try:
        cursor.execute(f"INSERT INTO users {tuple(sql_keys)} VALUES ({sql_values[:-2]})", parameters)
        with lock:
            db.commit()

    except sqlite3.IntegrityError:
        return

    return read_user(user.username)


def read_user(username: str) -> User | None:
    """Select the info of a user by his username"""

    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    user = cursor.fetchall()

    if not user:
        return

    return User(
        username = user[0][1],
        password = user[0][2],
        firstName = user[0][3],
        lastName = user[0][4],
        email = user[0][5],
        age = user[0][6],
        role = user[0][7]
    )


def update_user(username: str, update: User) -> User | None:
    """Update the info of this user in the database"""

    cursor.execute("SELECT * FROM users WHERE username = '%s'" % (username))
    user = cursor.fetchall()

    if not user:
        return

    for key in update.__dict__.keys():
        if update.__dict__[key]:
            cursor.execute(f"UPDATE users SET {key} = '{update.__dict__[key]}' WHERE id = '{user[0][0]}'")

    db.commit()

    return read_user(username if not update.username else update.username)


def delete_user(username: str) -> bool:
    """Delete a user from the database"""

    if not read_user(username):
        return False

    cursor.execute("DELETE FROM users WHERE username = '%s'" % (username))
    db.commit()

    return True


def read_all_users() -> list[dict]:
    """Read the info of all users"""

    cursor.execute("SELECT username from users")
    users = cursor.fetchall()

    users_list = []

    for user in users:
        users_list.append(read_user(user[0]))

    return users_list
