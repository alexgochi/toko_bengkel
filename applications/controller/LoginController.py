from flask_login import current_user, login_user, login_required, logout_user
from ..dao import LoginDao as loginDao
from .. import login_manager
from io import StringIO
from xhtml2pdf import pisa
import pytz
from time import sleep
from threading import Thread
from functools import wraps
import datetime
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask import current_app as app
from flask import request, render_template, make_response, request, jsonify, redirect, Blueprint, url_for, session
from flask import flash
from applications.model.user import DbUser


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is not None:
        user = loginDao.select_req(id=user_id)

    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Bypass if user is logged in
    print(" curr_user " + current_user.absen +
          " isAuth " + str(current_user.is_authenticated))
    ip_address = request.remote_addr

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        print(request.method)
        if request.method == 'POST':
            d = request.form.to_dict()
            absen = d["username"]
            pin = d["pin"]
            api = {"status": True, "msg": "Login Sukses"}
            user = loginDao.findById(absen, pin)
            print(user)

            if not user:
                api = {'status': False, "msg": "User atau Password salah"}

            if api["status"] == True:
                login_user(DbUser(user))
                print(" curr_user " + current_user.absen + " user_login " + absen)
                session["role"] = None
            return jsonify(api)

    return render_template("login.html")


@app.route('/')
@login_required
def index():
    return render_template("index.html")
