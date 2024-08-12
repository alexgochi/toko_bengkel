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
from applications.dao import ReceiptDao as receiptDao
from applications.dao import DashboardDao as dashboardDao
from applications.lib import dataTableError

@app.route('/receipt/', methods=['GET'])
@login_required
def receipt():
    data = receiptDao.get_data_distinct()
    return render_template('receipt.html', data=data)

@app.route("/dt/receipt", methods=["GET"])
def dt_receipt():
    res = receiptDao.dt_data_receipt(
        request.args.get("search"),
        request.args.get('start'),
        request.args.get('filter')
    )
    if res.is_error:
        return dataTableError()
    
    return jsonify({
        "data": res.result,
        "recordsFiltered": res.dt_total
    })

@app.route('/receipt/getAllData', methods=['GET'])
@login_required
def getAllDataReceipt():
    db_res = receiptDao.getAllDataReceipt()
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Get Data", "data":db_res.result})

@app.route('/addReceipt/', methods=['GET'])
@login_required
def addReceipt():
    outlet = dashboardDao.getDataOutlet().result
    return render_template("receipt-add.html", data_outlet=outlet)


@app.route('/receipt/save', methods=['POST'])
@login_required
def saveReceipt():
    data = request.get_json()
    db_res = receiptDao.save_receipt(data)
    if db_res.is_error:
        return jsonify({"status": db_res.status, "message": str(db_res.pgerror)})
    return jsonify({"status": db_res.status, "message": "Berhasil Simpan Data Draft"})

@app.route('/receipt/detail', methods=['GET'])
@login_required
def getDataRecByFaktur():
    data = request.args.get('faktur')
    print(data)
    db_res = receiptDao.getDataRecByFaktur(data)
    print(db_res)
    return db_res
