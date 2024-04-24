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
from applications.dao import ProductDao as productDao
from applications.lib import dataTableError


@app.route('/product/', methods=['GET'])
@login_required
def product():
    category = productDao.get_data_category().result
    outlet = productDao.get_data_outlet().result
    return render_template("product.html", data_cat=category, data_outlet=outlet)

@app.route('/product/getMerk', methods=['POST'])
@login_required
def get_merk():
    data = request.form.to_dict()
    db_res = productDao.get_data_merk(data['id'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", 'result': db_res.result})



@app.route("/dt/product/", methods=["GET"])
def dt_product():
    res = productDao.dt_data_product(
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

@app.route('/product/edit', methods=['POST'])
@login_required
def edit_product():
    data = request.form.to_dict()
    db_res = productDao.update_data_product(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Update data"})


@app.route('/product/delete', methods=['POST'])
@login_required
def delete_product():
    data = request.form.to_dict()
    db_res = productDao.delete_data_product(data['sku'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data"})


@app.route('/product/add', methods=['POST'])
@login_required
def add_product():
    data = request.form.to_dict()
    db_res = productDao.add_data_product(data)
    print("ini db res : ",db_res)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Tambah data"})