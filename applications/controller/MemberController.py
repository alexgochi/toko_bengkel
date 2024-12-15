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
from applications.dao.MemberDao import get_all_member, dt_data_member, update_data_member, delete_data_member, add_data_member, check_id_member
from applications.lib import dataTableError
from applications.controller.DashboardController import generate_pdf

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

@app.route('/member/edit', methods=['POST'])
@login_required
def edit_member():
    data = request.form.to_dict()
    db_res = update_data_member(data)
    if db_res.is_error:
        return jsonify({"status": False, "message": str(db_res.pgerror)})
    # kalau hasilnya cuma 1 (ambil index ke-0)
    index_0 = db_res.first
    return jsonify({"status": True, "message": "Berhasil Update data Member"})

@app.route('/member/delete', methods=['POST'])
@login_required
def delete_member():
    data = request.form.to_dict()
    db_res = delete_data_member(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data Member"})

@app.route('/member/checkId', methods=['POST'])
@login_required
def check_id():
    data = request.form.to_dict()
    db_res = check_id_member(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", 'result': db_res.first})

@app.route('/member/add', methods=['POST'])
@login_required
def add_member():
    data = request.form.to_dict()
    db_res = add_data_member(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Tambah data Member"})

@app.route('/member/downloadAllMember', methods=['GET'])
@login_required
def download_all_member():
    db_res = get_all_member()
    data = db_res.result
    if len(data) > 0:
        return jsonify({"status": True, "message": "Berhasil Get Data", "data":generate_pdf(data)})
    return jsonify({"status": False, "message": "Tidak Ada Data"})