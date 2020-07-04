from flask import Flask
from flask import session, redirect, url_for, request
from flask import render_template
from gallery.data.user import User
from gallery.data.db import connect
from gallery.data.postgres_user_dao import PostgresUserDAO
from gallery.tools.secrets import get_secret_flask_session
from functools import wraps


app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = get_secret_flask_session()["secret_key"]
# database connection
connect()


def get_user_dao():
    return PostgresUserDAO()


# fred is admin example in video, changed to admin
def check_admin():
    return 'username' in session and session['username'] == 'admin'

# function decorator - takes flask view as an argument, this decorator returns a new function that checks admin and does what the view would normally do. Removes duplication.


def requires_admin(view):
    @wraps(view)
    def decorated(**kwargs):
        if not check_admin():
            return redirect('/login')
        return view(**kwargs)
    return decorated


# **** Login Routes
# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_dao().get_user_by_username(
            request.form["username"])
        if user is None or user.password != request.form["password"]:
            return redirect('/invalidLogin')
        else:
            # store session data for user name
            session['username'] = request.form["username"]
            # -- debug route
            # return redirect('/debugSession')
            return render_template('users.html', users=get_user_dao().get_users())
    else:
        return render_template('login.html')


@app.route('/invalidLogin')
def invalidLogin():
    return "Invalid Login"


@app.route('/debugSession')
def debugSession():
    result = ""
    for key, value in session.items():
        result += key + "--" + str(value) + "<br/>"
    return result

# ----Main routes----
@app.route('/')
def main():
    render_template('login.html')


@app.route('/admin/users')
@requires_admin
def users():
    return render_template('users.html', users=get_user_dao().get_users())

# escape username with urlib.quote()
@app.route('/admin/deleteUser/<username>')
@requires_admin
def deleteUser(username):
    return render_template('confirm.html',
                           title="Confirm delete",
                           message="Are you sure you want to delete user?",
                           on_yes="/admin/executeDeleteUser/" + username,
                           on_no="/admin/users"
                           )


@app.route('/admin/executeDeleteUser/<username>')
@requires_admin
def executeDeleteUser(username):
    get_user_dao().delete_user(username)
    return redirect('/admin/users')
