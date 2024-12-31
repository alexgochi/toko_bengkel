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
from applications.dao import OutletDao as outletDao
from applications.lib import dataTableError
from applications.controller.DashboardController import generate_pdf

@app.route('/outlet/', methods=['GET'])
@login_required
def outlet():
    return render_template("outlet.html")

@app.route('/outlet/checkId/', methods=['POST'])
@login_required
def check_id_outlet():
    data = request.form.to_dict()
    db_res = outletDao.check_id_outlet(data['outlet_id'])
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
    db_res = outletDao.delete_data_outlet(data['outlet_id'])
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

# @app.route('/outlet/downloadAllOutletPdf', methods=['GET'])
# @login_required
# def download_all_outlet_pdf():
#     db_res = outletDao.get_all_outlet()
#     data = db_res.result
#     if len(data) > 0:
#         return jsonify({"status": True, "message": "Berhasil Get Data", "data":generate_pdf(data)})
#     return jsonify({"status": False, "message": "Tidak Ada Data"})

@app.route('/outlet/downloadAllOutlet', methods=['GET'])
@login_required
def download_all_outlet():
    res = outletDao.get_data_outlet_filter(
        request.args.get("search")
    )
    data = res.result
    message = ""
    if len(data) > 0:
        download, message = GlobalFunction.generateExcel('Outlet', data)
        if download:
            return jsonify({"status": True, "message": "Berhasil Download File"})
    return jsonify({"status": False, "message": f"Gagal Download File\n{message}"})
