from app import app
from flask import render_template
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from flask import Flask, url_for, redirect, flash

# changes
import time
from flask import request, redirect
import sched
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from app import socketio
from flask_socketio import SocketIO, send, emit
from pin_detect import test_pin_route
from track_eye import get_data
import threading
import trace
from my_constants import *


sch = BackgroundScheduler()
# sch.start()

# HOME PAGE
@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title='Eye Tracker Home')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def logIn():
    sch.start()
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user.username)
        print(user.password)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
        	next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


# RECORD PASSWORD (GRID)
@app.route('/recording')
def recording():
    # print(username)
    sch.add_job(pin, 'interval', seconds=2, id='pin_job')
    return render_template('recording.html', title='Record Password', pin=2)

# LOGIN
@app.route('/login_eye', methods=['GET', 'POST'])
def logInEye():
    # sch.remove_job('pin_job')
    print("login_eye")
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    
    form.password.data = test_pin_route("test.txt")
    # vars that are true if the user's speed and double mapping matches stored values
    user_speed = True
    user_dist = True

    print("pin: ", form.password.data)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user_speed or user_dist:
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))

        login_user(user)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
        	next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)



# LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def pin():
    print('yay')
    sch.remove_job('pin_job')
    get_data()
    print(pin)


# ignore for now:
# real time
def ack():
    print('message was received!')

    
@socketio.on('connect')
def on_connect():
    print('hi')
    emit('my response', {'data': "hello"}, callback=ack)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
