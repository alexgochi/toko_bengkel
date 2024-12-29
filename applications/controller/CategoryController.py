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
from applications.dao import CategoryDao as categoryDao
from applications.lib import dataTableError
from applications.controller.DashboardController import generate_pdf

@app.route('/category/', methods=['GET'])
@login_required
def category():
    # db_res = categoryDao.get_data_merk()
    # merk = db_res.result
    return render_template("category.html")

@app.route("/dt/category/", methods=["GET"])
def dt_category():
    res = categoryDao.dt_data_category(
        request.args.get("search"),
        request.args.get('start'),
        request.args.get('order_by')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/category/edit', methods=['POST'])
@login_required
def edit_category():
    data = request.form.to_dict()
    db_res = categoryDao.update_data_category(data)
    return db_res

@app.route('/category/delete', methods=['POST'])
@login_required
def delete_category():
    data = request.form.to_dict()
    db_res = categoryDao.delete_data_category(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data"})

@app.route('/category/add', methods=['POST'])
@login_required
def add_category():
    data = request.form.to_dict()
    db_res = categoryDao.add_data_category(data)
    return db_res

@app.route('/category/downloadAllMerkPdf', methods=['GET'])
@login_required
def download_all_merk_pdf():
    db_res = categoryDao.get_all_merk()
    data = db_res.result
    if len(data) > 0:
        return jsonify({"status": True, "message": "Berhasil Get Data", "data":generate_pdf(data)})
    return jsonify({"status": False, "message": "Tidak Ada Data"})

@app.route('/category/downloadAllMerk', methods=['GET'])
@login_required
def download_all_merk():
    res = categoryDao.get_data_category_filter(
        request.args.get("search"),
        request.args.get('order_by')
    )
    data = res.result
    for x in data:
        x['ID Merk'] = int(x['ID Merk'])
        x['Jumlah Kategori'] = int(x['Jumlah Kategori'])
    message = ""
    if len(data) > 0:
        download, message = GlobalFunction.generateExcel('Merk', data)
        if download:
            return jsonify({"status": True, "message": "Berhasil Download File"})
    return jsonify({"status": False, "message": f"Gagal Download File\n{message}"})
