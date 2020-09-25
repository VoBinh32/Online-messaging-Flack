import os

from collections import deque
from flask import Flask, render_template, session, request, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session

from helpers import login_required

app = Flask(__name__)
app.config["SECRET_KEY"] = "binhvo"
socketio = SocketIO(app)

# Create 2 lists and a dict for controlling
# all of the channels, users and messages for each channel
channels = []
users = []
messages = dict()


@app.route("/")
@login_required
def index():
    """Show the home with all of channel whenever user logged in"""
    return render_template("index.html", channels=channels)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any username
    session.clear()
    # Get the username from the form
    username = request.form.get("username")
    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return render_template("apology.html", message="you must provide a display name!")
        # Ensure each username is different
        if username in users:
            return render_template("apology.html", message="display name already exists!")
        # Add username to the global users list
        users.append(username)
        # Remember which user has logged in
        session['username'] = username
        # Remember the useron a cookie even if the browser is closed.
        session.permanent = True
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout", methods=['GET'])
def logout():
    """Log user in"""
    # When user log out, try to remove the user from the global list.
    try:
        users.remove(session['username'])
    except ValueError:
        pass
    # Forget any username
    session.clear()
    # Redirect to the login form
    return redirect("/")


@app.route("/create", methods=["POST","GET"])
def create():
    """ Create a channel and redirect to its page"""

    # Get the new channel from the form
    new_channel = request.form.get("channel")
    if request.method == "POST":
        # Make sure user type in a channel name
        if not new_channel:
            return render_template("apology.html", message="you must provide a channel name!")
        # Then add that new channel into the global channel list
        channels.append(new_channel)

        # Add channel to global dict of channels with messages
        # Every channel is a deque to use popleft() method 
        messages[new_channel] = deque()

        #Then redirect to the new page.
        return redirect("/channels/" + new_channel)
    else:
        return render_template("index.html", channels=channels)

@app.route("/channels/<channel>", methods=["GET"])
@login_required
def enter(channel):
    """Show the user the channel page"""

    #Update the current channel
    session["current_channel"] = channel
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("channel.html", channels=channels, messages=messages[channel])

@socketio.on("joined", namespace='/')
def joined():
    """ Send message to announce that user has entered the chat """

    # Get the current channel and save it into 'room'.
    room = session.get('current_channel')

    join_room(room)

    emit('status', {
        'users': session.get('username'),
        'channel': room,
        'msg': session.get('username') + " has entered the chat"},
        room=room)

@socketio.on("left", namespace='/')
def left():
    """ Send message to announce that user has left the chat """

    # Get the current channel and save it into 'room'.
    room =  session.get('current_channel')

    leave_room(room)

    emit('status', {
        'channel': room,
        'msg': session.get('username') + " just left the chat"}, 
        room=room)


@socketio.on("send message")
def send_msg(msg, timestamp):
    """"Broadcase the messages onto the channel"""

    room = session.get('current_channel')

    # Only store the 100 most recent messages per channel, if more than 100 then delete.
    if len(messages[room]) > 100:
        messages[room].popleft()

    messages[room].append([timestamp, session.get('username'), msg])

    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg}, 
        room=room)