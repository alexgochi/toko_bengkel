"""
    Modul untuk setting flask-login, kalau mau ubah tolong pelajari dulu flask-login + JWT ya :)
"""

from flask import g, redirect, flash, make_response, abort
from flask_login import user_loaded_from_request
from .fl_validator import validate_user, validate_user_api
from .utils import login_manager, detect_request_source, get_login_url


@login_manager.user_loader
def fl_user_loader(id_user: str):
    message, status_code, user_obj = validate_user(id_user)

    """
        ubah pgcode 08001 (sqlclient_unable_to_establish_sqlconnection) dari PostgresDatabse menjadi
        http code 500 (Internal Error)
    """
    status_code = 500 if status_code == "08001" else status_code
    if status_code != 200:
        abort(make_response(message.get("message"), 500))
    return user_obj


@login_manager.request_loader
def fl_request_loader(request):
    """
    Proses auth & authz ada 2 mode:
        1. Authorization header (by Bearer JWT)
        2. Browser cookie (by session)
    Kita coba satu2 dimulai dari "Bearer JWT", jika kosong maka lanjut coba pakai "session".
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return None

    api_token = auth_header.replace("Bearer ", "", 1)
    message, status_code, user_obj = validate_user_api(api_token)

    status_code = 500 if status_code == "08001" else status_code
    if status_code != 200:
        abort(make_response(message, status_code))

    return user_obj


@user_loaded_from_request.connect
def user_loaded_from_request(app, user=None):
    g.login_via_request = True


@login_manager.unauthorized_handler
def flask_login_unauthorized():
    """
    Handles authentication failure based on the request source.
    Returns:
        Flask.Response
            If the request is from Ajax or other sources, it returns a plain text response with 401 status_code.
            If the request is from a browser, it redirects to the login page (302).
    """
    request_source = detect_request_source()

    if request_source == "ajax":
        # TODO: Bikin logic jika request ajax maka suruh user login tanpa harus redirect ke halaman login
        return "Anda belum login aplikasi bnm!", 401
    elif request_source == "browser":
        flash("Anda belum login aplikasi bnm!")
        return redirect(get_login_url())
    else:
        return {"message": "Token tidak valid!"}, 401
