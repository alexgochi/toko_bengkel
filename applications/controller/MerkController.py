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
from applications.dao import MerkDao as merkDao
from applications.lib import dataTableError
from applications.controller.DashboardController import generate_pdf

@app.route('/merk/', methods=['GET'])
@login_required
def merk():
    db_res = merkDao.get_data_category()
    cat = db_res.result
    return render_template("merk.html", data_cat=cat)

@app.route("/dt/merk/", methods=["GET"])
def dt_merk():
    res = merkDao.dt_data_merk(
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

@app.route('/merk/edit', methods=['POST'])
@login_required
def edit_merk():
    data = request.form.to_dict()
    db_res = merkDao.update_data_merk(data)
    return db_res

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
    return db_res

# @app.route('/merk/downloadAllCategoryPdf', methods=['GET'])
# @login_required
# def download_all_category_pdf():
#     db_res = merkDao.get_all_category()
#     data = db_res.result
#     if len(data) > 0:
#         return jsonify({"status": True, "message": "Berhasil Get Data", "data":generate_pdf(data)})
#     return jsonify({"status": False, "message": "Tidak Ada Data"})

@app.route('/merk/downloadAllCategory', methods=['GET'])
@login_required
def download_all_category():
    res = merkDao.get_data_merk_filter(
        request.args.get("search"),
        request.args.get('order_by')
    )
    data = res.result
    for x in data:
        x['ID Merk'] = int(x['ID Merk'])
        x['ID Kategori'] = int(x['ID Kategori'])
        x['Jumlah Produk'] = int(x['Jumlah Produk'])
    message = ""
    if len(data) > 0:
        download, message = GlobalFunction.generateExcel('Kategori', data)
        if download:
            return jsonify({"status": True, "message": "Berhasil Download File"})
    return jsonify({"status": False, "message": f"Gagal Download File\n{message}"})
