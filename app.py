''' Sambadh Chat App
Author  : Samrat Adhikari
Date    : 14 March 2021
Purpose : Educational Purpose
'''

# ---------------------Modules------------------------------
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, join_room, leave_room
from flask_migrate import Migrate
from dotenv import load_dotenv
from time import strftime, localtime
from passlib.hash import pbkdf2_sha256 as hashpass
import os

from gevent import monkey
monkey.patch_all()

# ---------------------Custom Modules---------------------
from fields import RegistrationForm, LoginForm
from models import db, User

# -----------------Initialize flask app------------------
load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# ---------------------Configure database---------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db.init_app(app)
migrate = Migrate(app, db)

# -----------------------Initialize Flask-SocketIO--------------------
socketio = SocketIO(app, async_mode='gevent')
ROOMS = ['global', 'tech', 'history', 'philosophy', 'space']

# -------------------Configure flask login----------------------------
login = LoginManager(app)
login.init_app(app)

# -------------------For user login authentication--------------------
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------Routes-------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Hash the password
        hashed_pswd = hashpass.hash(password)

        # Add user to the database
        with app.app_context():
            user = User(username=username, password=hashed_pswd)
            db.session.add(user)
            db.session.commit()

        flash('Registered Successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=reg_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username=login_form.username.data).first()
        
        if user_object and hashpass.verify(login_form.password.data, user_object.password):
            login_user(user_object)
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', form=login_form)

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

# ------------------- SocketIO Event Buckets/Handlers--------------
@socketio.on('message')
def message(data):
    """Broadcast messages"""
    time_stamp = strftime('%b-%d %I:%M %p', localtime())
    send({'msg': data['msg'], 'username': data['username'], 'time_stamp': time_stamp}, room=data['room'])

@socketio.on('join')
def join(data):
    join_room(data['room'])
    if data['username']:
        send({'msg': f"{data['username']} has joined the {data['room']} room."}, room=data['room'])

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': f"{data['username']} has left the {data['room']} room."}, room=data['room'])

# --------------------------Run the program------------------------
if __name__ == '__main__':
    socketio.run(app)
    # app.run(debug=True)
