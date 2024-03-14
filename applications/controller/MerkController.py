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
from applications.dao import MerkDao as merkDao
from applications.lib import dataTableError


@app.route('/merk/', methods=['GET'])
@login_required
def merk():
    return render_template("merk.html")

@app.route("/dt/merk/", methods=["GET"])
def dt_merk():
    res = merkDao.dt_data_merk(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/merk/edit', methods=['POST'])
@login_required
def edit_merk():
    data = request.form.to_dict()
    db_res = merkDao.update_data_merk(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Update data"})


@app.route('/merk/delete', methods=['POST'])
@login_required
def delete_merk():
    data = request.form.to_dict()
    db_res = merkDao.delete_data_merk(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data"})


@app.route('/merk/add', methods=['POST'])
@login_required
def add_merk():
    data = request.form.to_dict()
    db_res = merkDao.add_data_merk(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Tambah data"})