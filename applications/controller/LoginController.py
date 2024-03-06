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
from flask import request, render_template, make_response, jsonify, redirect, Blueprint, url_for, session
from flask import flash
from applications.model.user import User
from applications.dao.LoginDao import dt_data_user
from applications.lib import dataTableError

@app.route("/dt/user", methods=["get"])
def dt_user():
    res = dt_data_user(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()


    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in upon page load."""
    if user_id is None:
        return None
    user = User()
    user.id = user_id
    return user


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # contoh pakai 
    from applications.dao.LoginDao import get_user_by_id
    user_id = "A001"
    db_res = get_user_by_id(user_id)
    if db_res.is_error:
        return db_res.pgerror
    elif db_res.is_empty:
        print("error bos..")
    # kalau hasilnya cuma 1 (ambil index ke-0)
    index_0 = db_res.first.get("user_name")
    index_1 = db_res.result[0]

    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            d = request.form.to_dict()
            absen = d["user_id"]
            pin = d["pin"]
            api = {"status": True, "msg": "Login Sukses"}
            user = loginDao.getLogin(absen, pin)
            print(user)

            if not user:
                api = {'status': False, "msg": "User atau Password salah"}

            if api["status"] == True:
                obj = User()
                obj.id = user[0]['user_id']
                obj.name = user[0]['name']
                obj.level = user[0]['level']
                login_user(obj)
                print(" curr_user " + current_user.id + " user_login " + absen)
                session["role"] = None
            return jsonify(api)
        list_user = loginDao.findUser()
        print(list_user)

    return render_template("login.html",list_user=list_user)


@app.route('/')
@login_required
def index():
    return render_template("index.html")

# logout process
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))