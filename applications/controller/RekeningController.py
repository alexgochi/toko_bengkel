from flask_login import current_user, login_user, login_required, logout_user
from applications.controller import GlobalFunction
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
from applications.dao import RekeningDao as rekDao
from applications.lib import dataTableError
from applications.controller.DashboardController import generate_pdf

@app.route('/rekening/', methods=['GET'])
@login_required
def rekening():
    return render_template("rekening.html")

@app.route("/dt/rek/", methods=["GET"])
def dt_rek():
    res = rekDao.dt_data_rekening(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/rek/edit', methods=['POST'])
@login_required
def edit_rek():
    data = request.form.to_dict()
    db_res = rekDao.update_data_rekening(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Update data"})

@app.route('/rek/delete', methods=['POST'])
@login_required
def delete_rek():
    data = request.form.to_dict()
    db_res = rekDao.delete_data_rekening(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data"})

@app.route('/rek/add', methods=['POST'])
@login_required
def add_rek():
    data = request.form.to_dict()
    print(data)
    db_res = rekDao.add_data_rekening(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Tambah Data"})

# @app.route('/rek/downloadAllRekPdf', methods=['GET'])
# @login_required
# def download_all_rek_pdf():
#     db_res = rekDao.get_all_rek()
#     data = db_res.result
#     if len(data) > 0:
#         return jsonify({"status": True, "message": "Berhasil Get Data", "data":generate_pdf(data)})
#     return jsonify({"status": False, "message": "Tidak Ada Data"})

@app.route('/rek/downloadAllRek', methods=['GET'])
@login_required
def download_all_rek():
    res = rekDao.get_data_rek_filter(
        request.args.get("search")
    )
    data = res.result
    for x in data:
        x['ID Rekening'] = int(x['ID Rekening'])
        x['Nomor Rekening'] = int(x['Nomor Rekening'])
    message = ""
    if len(data) > 0:
        download, message = GlobalFunction.generateExcel('Rekening', data)
        if download:
            return jsonify({"status": True, "message": "Berhasil Download File"})
    return jsonify({"status": False, "message": f"Gagal Download File\n{message}"})
