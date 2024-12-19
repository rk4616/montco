# https://www.freepik.com/icon/teepee-icon_11084426#fromView=search&page=1&position=27&uuid=70e1022f-4ca6-48d4-88dc-fd09139755db

import sqlite3
from urllib.parse import urljoin, urlparse, urlsplit

import flask
from flask import Flask, g, redirect, render_template, request
from flask_login import (LoginManager, UserMixin, login_required, login_user,
                         logout_user)


class User(UserMixin):
    def __init__(self, data):

        self.id = data["id"]
        self.username = data["username"]
        self.password = data["password"]

    def is_active(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


"""
So, without further ado, here's the theme: Odysseus has found himself in the middle of a grand scheme to invade 
Troy - finding himself stuck in a wooden horse en route to one of their most important cities, disguised as a 
gift to invade and conquer it. Build something (anything) that would help Odysseus during or after the journey 
inside the Trojan horse.

Be creative - it can be anything from something to entertain him during his journey, or something that provides 
genuine strategic value. We do value clever answers - as long as it justifiably fits the prompt, you're good!
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

# db = sqlite3.connect("app.db")


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect("app.db")

    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# https://flask.palletsprojects.com/en/stable/patterns/sqlite3/
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.cursor().executescript(f.read())
        db.commit()

def populate_users():
    with app.app_context():
        db = get_db()

        data = [
            ("odysseus", "horse", "commander"),
        ]
        for name in [
            "acamas",
            "agapetus",
            "agesipolis",
            "alekos",
            "alexandros",
            "alexis",
            "anastasius",
            "andreas",
            "antonios",
            "apollodorus",
            "aristophanes",
            "athanasius",
            "charalambos",
            "christos",
            "damon",
            "demetrius",
            "eustathius",
            "filippos",
            "georgios",
            "heraclitus"
        ]:
            data.append((name, "expendable", "soldier"))
        db.cursor().executemany("insert or ignore into users (username, password, role) values (?, ?, ?)", data)
        db.commit()


# with open("schema.sql") as f:
# db.cursor().executescript(f.read())


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    user = query_db("SELECT * FROM users WHERE id=?", (user_id,), one=True)
    if user is None:
        return None
    #print(str(user))
    return User(user)


@app.route("/")
def home():
    return render_template("index.html")


def url_has_allowed_host_and_scheme(url, host):
    # implement this similar to the Django function
    # Check if the URL is safe for redirects
    if not url or not host:
        return False

    # Parse the URL and join it with the host
    parsed_url = urlparse(url)
    base_url = urlparse(urljoin(request.host_url, url))

    # Check if the URL scheme and netloc match the request host
    return parsed_url.scheme in ("http", "https") and base_url.netloc == host


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(
            query_db("select * from users where username=?", [username], one=True)
        )
        print(user)
        if user and user.password == password:
            login_user(user)

            next = request.args.get("next")

            if next and urlsplit(next).netloc != "":
                return flask.abort(400)

            return flask.redirect(next or flask.url_for("protected"))

        return "not logged in"

    return render_template("auth/login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(flask.url_for("home"))


@app.route("/protected")
@login_required
def protected():
    return "hidden webpage <a>href='/logout'>logout</a>"


if __name__ == "__main__":
    app.run(debug=True, port=8000)
