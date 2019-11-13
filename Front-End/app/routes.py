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
from pin_detect import test_pin_route
# from track_eye import get_data
import threading
import trace
from my_constants import *
import socket
import os
import subprocess
import joblib
from eye_behaviors import check_eye_behavior
from distance import eyenalysis


sch = BackgroundScheduler()
sch.start()

IS_CALLIBRATED = False
get_data_loop = True


def get_data():

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        a = 0
        file_name = "test.txt"

        # if os.path.exists(file_name):
        #     print('remove')
        #     os.remove(file_name)

        f = open(file_name, "w")
        global get_data_loop
        while get_data_loop:
            # data = json.dumps(CHECK_CALIBRATION)
            data = " "
            sock.sendall(bytes(data + "\n", "utf-8"))

            # Receive data from the server and shut down
            received = str(sock.recv(1000), "utf-8")
            
            # print("Sent:     {}".format(data))
            # print("Received: {}".format(received))
            
            f.write(received)
            a+=1
    print(a)
    print("closed")
    f.close()
    if os.path.exists(file_name):
            print('yay file!')


# HOME PAGE
@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html', title='Eye Tracker Home')

# sch.start()
# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def logIn():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    try:
        os.system("taskkill /IM EyeTribeUIWin.exe")
    except:
        x=2
    

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
    
    sch.add_job(pin, 'interval', seconds=1, id='pin_job')
    global get_data_loop
    get_data_loop = True
    return render_template('recording.html', title='Record Password', pin=2)

# LOGIN
@app.route('/login_eye', methods=['GET', 'POST'])
def logInEye():
    
    global get_data_loop
    get_data_loop = False
    time.sleep(1)
    print("login_eye")
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    file_name="test.txt"
    form.password.data, pd_data = test_pin_route(file_name)
        # vars that are true if the user's speed and double mapping matches stored values
        
    user_speed = True# check_eye_behavior(form.username.data, pd_data)
    # print(user_speed)
    # not b/c not want to login if it detects not kendall
    user_dist = eyenalysis(file_name)
    # print(user_dist)
    # user_dist = not user_dist

    print("pin: ", form.password.data)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("check: ", user.check_password(form.password.data))
        # if not user_speed or not user_dist:
        if user is None or not user.check_password(form.password.data) or not user_speed or not user_dist:
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

# Calibrate
@app.route('/calibrate')
def calibrate():
    # add this to the scheduler/threader
    sch.add_job(check_calibration, 'interval', seconds=0.5, id='calibrate_job')

    return render_template('calibrate.html', title='Calibrate')


def check_calibration():
    sch.remove_job('calibrate_job')
    # global IS_CALLIBRATED
    # if not IS_CALLIBRATED:
    subprocess.Popen(CALLIBRATION_EXE)
    
        # IS_CALLIBRATED = True
    return

# @app.route('/pin')
def pin():
    print('yay')
    sch.remove_job('pin_job')
    get_data()
    print(pin)

