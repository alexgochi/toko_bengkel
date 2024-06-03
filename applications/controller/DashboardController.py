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
from applications.dao import DashboardDao as dashboardDao
from applications.lib import dataTableError

@app.route('/dashboard/getDataBySkuBarcode', methods=['GET'])
@login_required
def getDataBySkuBarcode():
    data = request.args.get('input')
    db_res = dashboardDao.getDataBySkuBarcode(data.upper())
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", "data":db_res.result})

@app.route('/dashboard/getDataLovProduct', methods=['GET'])
@login_required
def getDataLovProduct():
    db_res = dashboardDao.getDataLovProduct()
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", "data":db_res.result})

@app.route('/dt/lovProduct', methods=['GET'])
@login_required
def dt_lovProduct():
    res = dashboardDao.dt_lovProduct(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/dashboard/getMemberById', methods=['GET'])
@login_required
def getMemberById():
    id = request.args.get("id")
    db_res = dashboardDao.getDataMemberById(id)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", 'result': db_res.result})

@app.route('/addOrder/', methods=['GET'])
@login_required
def addOrder():
    member = dashboardDao.getDataMember().result
    outlet = dashboardDao.getDataOutlet().result
    paymentType = dashboardDao.getPaymentType().result
    rekening = dashboardDao.getRekening().result
    return render_template("order.html", data_outlet=outlet, data_member=member,data_type=paymentType,data_rek=rekening)

@app.route('/editOrder/<Faktur>', methods=['GET'])
@login_required
def editOrder(Faktur):
    member = dashboardDao.getDataMember().result
    outlet = dashboardDao.getDataOutlet().result
    paymentType = dashboardDao.getPaymentType().result
    rekening = dashboardDao.getRekening().result
    return render_template("orderEdit.html", faktur=Faktur, data_outlet=outlet, data_member=member,data_type=paymentType,data_rek=rekening)

@app.route('/detailOrder/<Faktur>', methods=['GET'])
@login_required
def detailOrder(Faktur):
    member = dashboardDao.getDataMember().result
    outlet = dashboardDao.getDataOutlet().result
    paymentType = dashboardDao.getPaymentType().result
    rekening = dashboardDao.getRekening().result
    return render_template("orderDetail.html", faktur=Faktur, data_outlet=outlet, data_member=member,data_type=paymentType,data_rek=rekening)


@app.route('/getDataFaktur/', methods=['GET'])
@login_required
def getDataFaktur():
    db_res = dashboardDao.getTransDraftData(request.args.get("faktur"))
    if not db_res:
        return jsonify({"status": False, "message": 'Data Tidak ditemukan',"data" : {}})
    return jsonify({"status": True, "message": "Berhasil Simpan Data Draft", "data" : db_res})

@app.route("/dt/dashboard/", methods=["GET"])
def dt_dashboard():
    res = dashboardDao.dt_data_dashboard(
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

@app.route('/dashboard/saveDraft', methods=['POST'])
@login_required
def saveDraft():
    data = request.get_json()
    data['status'] = False
    db_res,faktur = dashboardDao.save_order(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Simpan Data Draft"})

@app.route('/dashboard/saveInvoice', methods=['POST'])
@login_required
def saveInvoice():
    data = request.get_json()
    data['status'] = True
    db_res, faktur = dashboardDao.save_order(data, 'invoice')
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Simpan Data", "faktur":faktur})

@app.route('/dashboard/edit', methods=['POST'])
@login_required
def edit_dashboard():
    data = request.form.to_dict()
    db_res = dashboardDao.update_data_dashboard(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Update data"})


@app.route('/dashboard/delete', methods=['POST'])
@login_required
def delete_dashboard():
    data = request.form.to_dict()
    db_res = dashboardDao.delete_data_dashboard(data['faktur'])
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Hapus data"})


@app.route('/dashboard/add', methods=['POST'])
@login_required
def add_dashboard():
    data = request.form.to_dict()
    db_res = dashboardDao.add_data_dashboard(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Tambah data"})