import os
import time

from collections import deque
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "binhvo"
socketio = SocketIO(app)

channels = []
users = []
my_messages = dict()


@app.route("/")
@login_required
def index():
    return render_template("index.html", channels=channels)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    username = request.form.get("username")
    if request.method == "POST":
        if not username:
            return render_template("apology.html", message="you must provide a display name!")
        if username in users:
            return render_template("apology.html", message="display name already exists!")
        
        users.append(username)
        session['username'] = username
        session.permanent = True

        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/logout", methods=['GET'])
def logout():
    users.remove(session['username'])

    session.clear()
    return redirect("/")


@app.route("/create", methods=["POST"])
def create():
    new_channel = request.form.get("channel")
    if not new_channel:
        return render_template("apology.html", message="you must provide a channel name!")
    if new_channel in channels:
        return render_template("apology.html", message="channel name already exits!")
        
    channels.append(new_channel)
    my_messages[new_channel] = deque()

    return redirect("/channels/" + new_channel)