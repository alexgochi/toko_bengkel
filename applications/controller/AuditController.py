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
from applications.dao import AuditDao as auditDao
from applications.dao import DashboardDao as dashboardDao
from applications.dao import ProductDao as productDao
from applications.lib import dataTableError

@app.route('/audit/', methods=['GET'])
@login_required
def audit():
    paymentType = dashboardDao.getPaymentType().result
    rekening = dashboardDao.getRekening().result
    outlet = productDao.get_data_outlet().result
    return render_template('audit.html',data_outlet=outlet, data_rek=rekening, data_type=paymentType)

@app.route("/dt/audit", methods=["GET"])
def dt_audit():
    res = auditDao.dt_data_audit(
        request.args.get("search"),
        request.args.get("member"),
        request.args.get('start'),
        request.args.get('filter')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/audit/getAllDataAudit', methods=['GET'])
@login_required
def getAllDataAudit():
    db_res = auditDao.getAllDataAudit()
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", "data":db_res.result})

@app.route('/audit/getDataAuditByFaktur/<Faktur>', methods=['GET'])
@login_required
def getDataAuditByFaktur(Faktur):
    db_res = auditDao.getDataAuditByFaktur(Faktur)
    db_res['data']['print_date'] = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

    # set number with commas
    db_res['data']['other_fee'] = '{:,}'.format(db_res['data']['other_fee'])
    db_res['data']['total_faktur'] = '{:,}'.format(db_res['data']['total_faktur'])
    db_res['data']['diskon'] = '{:,}'.format(db_res['data']['diskon'])
    
    total_faktur = int(db_res['data']['total_faktur'].replace(',','')) + int(db_res['data']['other_fee'].replace(',','')) - int(db_res['data']['diskon'].replace(',',''))
    db_res['data']['total_faktur'] = '{:,}'.format(total_faktur)
    
    for x in db_res['data']['product']:
        x['qty'] = '{:,}'.format(x['qty'])
        x['price'] = '{:,}'.format(x['price'])
        x['subtotal'] = '{:,}'.format(x['subtotal'])

    return render_template('invoice.html', data=db_res['data'])

@app.route('/audit/getDetailDataAudit', methods=['GET'])
@login_required
def getDetailDataAudit():
    db_res = auditDao.getDataAuditByFaktur(request.args.get('faktur'))
    if db_res['status']:
        for x in db_res['data']['product']:
            x['qty'] = '{:,}'.format(x['qty'])
            x['price'] = '{:,}'.format(x['price'])
            x['subtotal'] = '{:,}'.format(x['subtotal'])

    return jsonify(db_res)


@app.route('/audit/updatePaymentAudit', methods=['POST'])
@login_required
def updatePaymentAudit():
    data = request.get_json()
    db_res = auditDao.update_payment_audit(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Update Data Pembayaran"})