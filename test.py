# https://www.freepik.com/icon/trojan-horse_9056237#fromView=search&page=1&position=5&uuid=46103ca8-cbc0-4ca2-9fd3-a43b82c46f78
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

class Event:
    def __init__(self, id, title, description, assigned_to):
        self.id = id
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self._status = 0
        self.log = ""

    @property
    def color(self):
        if self._status == 0:
            return "red"
        elif self._status == 1:
            return "yellow"
        elif self._status == 2:
            return "green"
        return "black"
    
    @property
    def status(self):
        return ["Not Started", "In Progress", "Completed"][self._status]
    

events = [
     Event(1, "Destroy the War Tents", """
          Soldiers are tasked with setting fire to the enemy's war tents, effectively dismantling their command structure and disrupting their ability to organize.
          This operation is crucial for sowing confusion and weakening the morale of the Trojan forces, as their leaders will be left without a central place to meet and plan. 
          The soldiers must be swift and precise, ensuring the flames spread quickly while avoiding unnecessary confrontation. 
          The goal is not to engage in direct combat, but to create chaos and instill fear in the hearts of the enemy.""", 2),
    Event(2, "Clear the Market", """
Soldiers are tasked with clearing the market square of all civilians, ensuring they return to their homes. 
This operation is crucial to maintain order and prevent any interference with the strategic movements of the troops.
The soldiers must be firm yet fair, avoiding unnecessary violence while ensuring compliance.
""", 1),
   
    Event(3,"Capture Priam's Palace", """
          Soldiers are tasked with infiltrating and capturing Priam’s palace, the symbolic heart of Troy and the residence of its king. 
          This operation is critical to strike at the core of Trojan leadership, undermining their confidence and breaking their will to fight. 
          The soldiers must advance under the cover of darkness, neutralizing guards and securing key areas of the palace with precision. 
          The objective is to seize control without unnecessary bloodshed, capturing any valuable intelligence and ensuring the king’s presence is rendered irrelevant to the Trojan war effort.""", 3),
        Event(4, "Burn Petraikos", """
              Soldiers are tasked with setting fire to Petraikos, a strategically located Trojan village that serves as both a supply hub and a rest point for troops. 
              This operation is vital for disrupting the Trojan’s local resources, cutting off their access to food, shelter, and reinforcements. 
              The soldiers must target the village's key structures—homes, granaries, and any stockpiled goods—ensuring that the fire spreads rapidly and destroys everything of value. 
              The goal is to demoralize the Trojan forces by leaving them with fewer places to rest and replenish. 
              Precision is key: the operation should be executed swiftly and without engaging the enemy directly. 
              After the fire is set, the soldiers should retreat quickly, minimizing the risk of Trojan retaliation or counterattacks.""", 8),
        Event(5,"Burn Field 1", "", 4),
        Event(6, "Burn Field 2", "", 5),
        Event(7, "Burn Athenion", """
          Soldiers are tasked with setting fire to Athenion, a key supply depot used by the Trojans to store weapons, armor, and other critical military resources. 
          This operation is essential for crippling their war machine, rendering them unable to equip their forces effectively for the battles ahead. 
          The soldiers must ensure that the fire spreads quickly through the storage areas, reducing the Trojans' ability to replace damaged equipment and weakening their overall combat readiness. 
          Timing and precision are crucial; the objective is to cause maximum damage without alerting the enemy prematurely. The soldiers should avoid unnecessary confrontation and retreat swiftly after the strike to minimize exposure to Trojan forces.""", 6),
    Event(8, "Burn Kallisto", """
          Soldiers are tasked with setting fire to Kallisto, a crucial Trojan military outpost used for staging troops and storing provisions. 
          This operation aims to disrupt their strategic operations, preventing the Trojans from launching coordinated attacks and weakening their logistical support. 
          The soldiers must target the warehouses, tents, and any supplies that would fuel the enemy's war efforts. 
          The fire should be set with precision to cause maximum destruction, but without drawing attention too early. 
          The goal is to cripple the Trojans' readiness, forcing them to divert resources to salvage their outpost while we remain out of sight, retreating before they can mount an effective counterattack.""", 7),
   
    Event(10, "Burn Vasiliki", """
          Soldiers are tasked with setting fire to Vasiliki, a Trojan village that serves as an important agricultural and logistical center, supplying the enemy with food and materials. 
          This operation is designed to cripple the Trojans' ability to sustain their army, making it more difficult for them to feed and equip their forces. 
          The soldiers must focus on destroying the granaries, barns, and storage facilities, ensuring that the flames consume the village's essential resources. 
          The goal is to cause widespread panic and disarray within the Trojan ranks, as their supply lines are severely disrupted. 
          Stealth and speed are paramount; the attack must be executed under cover of night, with minimal direct confrontation to avoid alerting enemy scouts. 
          Once the fire is set, the soldiers should retreat quickly, leaving the village in ruins and the Trojans scrambling to recover.""", 9),
    Event(9, "Burn Thalassa", """
          Soldiers are tasked with setting fire to Thalassa, a key inland Trojan village known for its storage of grain, livestock, and other essential provisions. 
          This operation is designed to disrupt the Trojans' food supply and create scarcity within their ranks. 
          By destroying Thalassa, we aim to cripple their ability to sustain their forces, forcing them to divert troops and resources to recover from the loss. 
          The soldiers must focus on burning the granaries, barns, and any stockpiled goods, ensuring the flames consume the village’s vital resources. 
          The goal is to leave the Trojans without immediate access to food and supplies, weakening their morale and their ability to fight. 
          The operation must be swift and executed under the cover of night, with minimal direct conflict. 
          After setting the fire, the soldiers must retreat quickly to avoid retaliation and remain undetected.""", 10),
]

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
    return User(user)


@app.route("/")
def home():
    soldiers = query_db("SELECT * FROM users WHERE role='soldier'")

    # compute progress
    num_events = len(events)
    total = num_events * 2
    progress = sum(event._status for event in events)


    return render_template("index.html", events=events, soldiers=soldiers, progress=(progress/total))


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

@app.route("/event/<_id>", methods=["GET", "POST"])
def event(_id):
    if not _id:
        return "Event ID is required", 400

    if not _id.isdigit():
        return "Invalid Event ID", 400

    event = [elem for elem in events if elem.id == int(_id)][0]
    if not event:
        return "Event not found", 404
    
    print(event.assigned_to)
    soldier = query_db("select * from users where id=?", [event.assigned_to], one=True)
    if not soldier:
        return "Assigned soldier not found", 404
    
    if request.method == "POST":
        status = request.form.get("status")
        
        if status:
            event._status = int(status)
        
        event.log = request.form.get("log")

        return redirect("/")

    return render_template("event.html", event=event, soldier=soldier)

@app.route("/event_colors")
def colors():
    ret = {}
    for event in events:
        ret[event.id] = event.color
    
    return ret


if __name__ == "__main__":
    app.run(debug=True, port=8000)
