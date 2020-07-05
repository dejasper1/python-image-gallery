from .user_dao import UserDAO
from .user import User
from . import db


class PostgresUserDAO(UserDAO):
    def __init__(self):
        pass

    # implementation of interface from defined in user dao
    def get_users(self):
        result = []
        cursor = db.execute("select username,password,full_name from users")
        for t in cursor.fetchall():
            result.append(User(t[0], t[1], t[2]))
        return result

    # implementation of interface from defined in user dao
    def get_single_user(self, username):
        cursor = db.execute(
            "select username,password,full_name from users where username=%s", (username,))
        row = cursor.fetchone()
        if row is None:
            return None
        else:
            return User(row[0], row[1], row[2])

    # implementation of interface from defined in user dao
    def delete_user(self, username):
        db.execute("delete from users where username=%s", (username,))

    # implementation of interface from defined in user dao

    def create_user(self, username, password, full_name):
        db.execute("insert into users (username, password, full_name) values (%s, %s, %s);",
                   (username, password, full_name))

    # implementation of interface from defined in user dao
    def edit_user(self, username, password, full_name):
        if not(full_name):
            db.res = execute(
                "update users set password = %s where username=%s;", (password, username))
        if not(password):
            db.execute(
                "update users set full_name = %s where username=%s;", (full_name, username))
