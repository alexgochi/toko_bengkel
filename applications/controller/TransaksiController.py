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
from applications.dao import TransaksiDao as transaksiDao
from applications.lib import dataTableError

@app.route('/transaksi/', methods=['GET'])
@login_required
def transaksi():
    return render_template('transaksi.html')

@app.route("/dt/transaksi", methods=["GET"])
def dt_transaksi():
    res = transaksiDao.dt_data_trans(
        request.args.get("search"),
        request.args.get('start')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/transaksi/getAllData', methods=['GET'])
@login_required
def getAllDataTransaksi():
    db_res = transaksiDao.getAllDataTransaksi()
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", "data":db_res.result})

@app.route('/transaksi/getDataTransByFaktur/<Faktur>', methods=['GET'])
@login_required
def getDataTransByFaktur(Faktur):
    db_res = transaksiDao.getDataTransByFaktur(Faktur)
    db_res['data']['print_date'] = datetime.datetime.now().strftime("%d-%m-%Y  %H:%M:%S")

    # set number with commas
    db_res['data']['other_fee'] = '{:,}'.format(db_res['data']['other_fee'])
    db_res['data']['total_faktur'] = '{:,}'.format(db_res['data']['total_faktur'])
    
    total_faktur = int(db_res['data']['total_faktur'].replace(',','')) + int(db_res['data']['other_fee'].replace(',',''))
    db_res['data']['total_faktur'] = '{:,}'.format(total_faktur)
    
    for x in db_res['data']['product']:
        x['qty'] = '{:,}'.format(x['qty'])
        x['price'] = '{:,}'.format(x['price'])
        x['subtotal'] = '{:,}'.format(x['subtotal'])

    return render_template('invoice.html', data=db_res['data'])

@app.route('/transaksi/getDetailDataTrans', methods=['GET'])
@login_required
def getDetailDataTrans():
    db_res = transaksiDao.getDataTransByFaktur(request.args.get('faktur'))
    if db_res['status']:
        for x in db_res['data']['product']:
            x['qty'] = '{:,}'.format(x['qty'])
            x['price'] = '{:,}'.format(x['price'])
            x['subtotal'] = '{:,}'.format(x['subtotal'])

    return jsonify(db_res)