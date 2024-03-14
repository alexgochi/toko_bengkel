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
from applications.dao import OutletDao as outletDao
from applications.lib import dataTableError


@app.route('/outlet/', methods=['GET'])
@login_required
def outlet():
    return render_template("outlet.html")

@app.route('/outlet/checkId/', methods=['POST'])
@login_required
def check_id_outlet():
    data = request.form.to_dict()
    db_res = outletDao.check_id_outlet(data['id'])
    print(db_res)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", 'result': db_res.first})

@app.route("/dt/outlet/", methods=["GET"])
def dt_outlet():
    res = outletDao.dt_data_outlet(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/outlet/edit', methods=['POST'])
@login_required
def edit_outlet():
    data = request.form.to_dict()
    db_res = outletDao.update_data_outlet(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Update data"})


@app.route('/outlet/delete', methods=['POST'])
@login_required
def delete_outlet():
    data = request.form.to_dict()
    db_res = outletDao.delete_data_outlet(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data"})


@app.route('/outlet/add', methods=['POST'])
@login_required
def add_outlet():
    data = request.form.to_dict()
    db_res = outletDao.add_data_outlet(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Tambah data"})