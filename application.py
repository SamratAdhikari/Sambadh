''' Sambadh Chat App
Author  : Samrat Adhikari
Date    : 14 March 2021
Purpose : Educational Purpose
'''


# ---------------------Modules------------------------------
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import localtime, strftime
import os

# ---------------------Custom Modules---------------------
from fields import *
from models import *


# -----------------Initialize flask app------------------
app = Flask(__name__)
# app.secret_key = os.environ.get('SECRET')
app.secret_key = 'secret key'


# ---------------------Configure database---------------------
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zehechgavwbcuh:d890a5f6d43d39fc3ca182eeee804276f6fe07b5657a8a0429d5749692ebdb6c@ec2-52-7-115-250.compute-1.amazonaws.com:5432/dcfi239smvt38i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# -----------------------Initialize Flask-SocketIO--------------------
socketio = SocketIO(app)
ROOMS = ['global', 'backbenchers', 'personal', 'coding']


# -------------------Configure flask login----------------------------
login = LoginManager(app)
login.init_app(app)


# -------------------For user login authentication--------------------
@login.user_loader
def load_user(id):

    return User.query.get(int(id))


# -------------------------------Routes-------------------------------
# Route for index/home
@app.route('/')
def index():
    return render_template('index.html')


# Route for registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pswd = hashpass.hash(password)
        # hashpass.using(rounds=29000, salt_size=16).hash(password)

        # Add user to database
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Registered Successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)


# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Allow login if validation is success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)

        return redirect(url_for('chat'))

    return render_template('login.html', form=login_form)


# Route for Chat Page
@app.route('/chat', methods=['GET', 'POST'])
# @login_required
def chat():

    if not current_user.is_authenticated:
        flash('Please Login first', 'danger')
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)


# Route for contact
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Route to Logout
@app.route('/logout', methods=['GET'])
def logout():

    logout_user()
    return redirect(url_for('index'))


# ------------------- SocketIO Event Buckets/Handlers--------------
# Message bucket
@socketio.on('message')
def message(data):
    """Broadcast messages"""
    # print(f"\n\n\n{data}\n\n\n")
    time_stamp = strftime('%b-%d %I:%M %p', localtime())
    send({'msg': data['msg'], 'username': data['username'],
          'time_stamp': time_stamp}, room=data['room'])


# Join a room
@socketio.on('join')
def join(data):

    join_room(data['room'])
    if data['username'] != '':
        send({'msg': data['username'] + " has joined the " +
              data['room'] + " room."}, room=data['room'])

# Leave a room
@socketio.on('leave')
def leave(data):

    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " +
          data['room'] + " room."}, room=data['room'])


# --------------------------Run the program------------------------
if __name__ == '__main__':
    # app.run()
    socketio.run(app)
