from flask_login import current_user, login_user, login_required, logout_user
from ..dao import LoginDao as loginDao
from .. import login_manager
from io import StringIO
# from xhtml2pdf import pisa
# import pytz
from time import sleep
from threading import Thread
from functools import wraps
import datetime
# import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask import current_app as app
from flask import request, render_template, make_response, jsonify, redirect, Blueprint, url_for, session
from applications.dao.MemberDao import dt_data_member
from applications.lib import dataTableError


@app.route('/member/', methods=['GET'])
@login_required
def member():
    return render_template("member.html")

@app.route("/dt/member", methods=["GET"])
def dt_user():
    res = dt_data_member(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })