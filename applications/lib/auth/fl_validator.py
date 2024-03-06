from typing import Tuple, Union
from application import Config
from .fl_repository import (
    get_data_user_rekanan,
    get_data_user_service_internal,
    getDataUserSAT,
    getDataUserKontraktor,
    getDataMenuUserKontraktor,
    getDataMenuUserSAT,
)
from .fl_model import ServiceInternal, UserAlfa, UserKontraktor, UserRekanan
import traceback
import jwt
from os import getenv

INTERNAL_ERROR = {"message": "Terjadi kesalahan internal!"}, 500, None
DB_CONNECTION_FAILURE = {"message": "Koneksi ke database error!"}, "08001", None


def validate_user(
    id_user: str,
) -> Tuple[str, Union[int, str], Union[UserAlfa, UserKontraktor, UserRekanan, None]]:
    """
    Validates a BMT user, whether it's a contractor (UserKontraktor) or SAT user (UserAlfa) or Rekanan user (UserRekanan).

    Args:
        id_user (str): The user ID, which can be either NIK ('22115966') or contractor code ('SAT.BD.K.0009').

    Returns:
        Tuple[str, int, Union[UserAlfa, UserKontraktor, None]]: A tuple containing the following elements:
            - message (str): A message related to the user validation.
            - status_code (int): The HTTP status code (500, 200, etc), or pgcode (08001)
            - user_obj (Union[UserAlfa, UserKontraktor, None]): If status is True, it contains the user object, if status is False, it is None.
    """

    # Deteksi login user SAT atau Kontraktor.
    # Kode kontraktor pasti dimulai dgn SAT.B.K, contoh: SAT.BD.K.0002
    # Kode rekanan pasti dimuoai dgn  SAT.R., cotoh: SAT.R.0001
    if str(id_user).startswith("SAT.BD.K."):
        return validate_user_kontraktor(id_user)
    elif str(id_user).startswith("SAT.R."):
        return validate_user_rekanan(id_user)
    else:
        return validate_user_alfa(id_user)


def validate_user_alfa(nik: str) -> Tuple[str, Union[int, str], Union[UserAlfa, None]]:
    # TODO: Buat logic multi company (SAT, MIDI, LWS, etc).
    try:
        # Get data user SAT
        hasil = getDataUserSAT(nik)
        if hasil.sqlclient_unable_to_establish_sqlconnection:
            return DB_CONNECTION_FAILURE
        elif hasil.is_error:
            return INTERNAL_ERROR
        elif hasil.is_empty:
            return "NIK Tidak Terdaftar!", 404, None
        user_sat = hasil.first

        # Validasi apakah user masih aktif
        if not user_sat["is_active"]:
            return "Akun anda telah di-nonaktifkan oleh admin!", 403, None

        # Validasi selesai, lanjut get menu user SAT
        hasil = getDataMenuUserSAT(user_sat["kode_jabatan"])
        if hasil.sqlclient_unable_to_establish_sqlconnection:
            return DB_CONNECTION_FAILURE
        elif hasil.is_error:
            return INTERNAL_ERROR

        menu = hasil.first["hasil"]["menu"]
        menu_role = hasil.first["hasil"]["menu_role"]

        # Instantiate user object
        user_obj = UserAlfa(
            user_sat["nik"],
            user_sat["nama_karyawan"],
            user_sat["kode_cabang"],
            user_sat["kode_jabatan"],
            user_sat["nama_jabatan"],
            menu,
            menu_role,
        )

        return "OK", 200, user_obj
    except Exception:
        traceback.print_exc()
        return INTERNAL_ERROR


def validate_user_kontraktor(
    kode_kontraktor: str,
) -> Tuple[bool, str, int, Union[UserKontraktor, None]]:
    try:
        # Get data user kontraktor
        hasil = getDataUserKontraktor(kode_kontraktor)
        if hasil.sqlclient_unable_to_establish_sqlconnection:
            return DB_CONNECTION_FAILURE
        elif hasil.is_error:
            return INTERNAL_ERROR
        elif hasil.is_empty:
            return "Kontraktor Tidak Terdaftar!", 404, None
        user_kontraktor = hasil.first

        # Validasi apakah kontraktor masih aktif
        if user_kontraktor["status"] != "T":
            return "Akun kontraktor ini telah di-nonaktifkan oleh admin!", 403, None

        # Validasi selesai, lanjut get menu kontraktor
        hasil = getDataMenuUserKontraktor()
        if hasil.sqlclient_unable_to_establish_sqlconnection:
            return DB_CONNECTION_FAILURE
        elif hasil.is_error:
            return INTERNAL_ERROR
        menu = hasil.first["hasil"]

        # Instantiate user object
        user_obj = UserKontraktor(
            user_kontraktor["kode_kontraktor"],
            user_kontraktor["nama_kontraktor"],
            user_kontraktor["nama_penanggung"],
            user_kontraktor["list_cabang"],
            menu,
        )

        return "OK", 200, user_obj
    except Exception:
        traceback.print_exc()
        return INTERNAL_ERROR


def validate_user_rekanan(
    kode_rekanan: str,
) -> Tuple[bool, str, int, Union[UserRekanan, None]]:
    # TODO: Buat logic multi company (SAT, MIDI, LWS, etc).
    try:
        # Get data user SAT
        hasil = get_data_user_rekanan(kode_rekanan)
        if hasil.sqlclient_unable_to_establish_sqlconnection:
            return DB_CONNECTION_FAILURE
        elif hasil.is_error:
            return INTERNAL_ERROR
        elif hasil.is_empty:
            return "Rekanan Tidak Terdaftar!", 404, None
        user_rekanan = hasil.first

        # Validasi apakah user masih aktif
        if not user_rekanan["is_active"]:
            return "Akun anda telah di-nonaktifkan oleh admin!", 403, None

        # Instantiate user object
        user_obj = UserRekanan(
            user_rekanan["kode_rekanan"],
            user_rekanan["alias"],
            user_rekanan["is_b2b"],
            user_rekanan["need_validate"],
            user_rekanan["list_cabang"],
        )

        return "OK", 200, user_obj
    except Exception:
        traceback.print_exc()
        return INTERNAL_ERROR


def validate_user_service_internal(
    service_id,
) -> Tuple[bool, str, int, Union[ServiceInternal, None]]:
    try:
        # get data user service intenral
        hasil = get_data_user_service_internal(service_id)
        if hasil.sqlclient_unable_to_establish_sqlconnection:
            return DB_CONNECTION_FAILURE
        elif hasil.is_error:
            return INTERNAL_ERROR
        elif hasil.is_empty:
            return f"Service Internal '{service_id}' Tidak Ditemukan!", 404, None

        # Validasi apakah service internal masih aktif ?
        if not hasil.first["is_active"]:
            return (
                f'Service "{service_id}" sudah di-nonaktifkan oleh admin!',
                403,
                None,
            )

        # Instantiate user object
        user_obj = ServiceInternal(hasil.first["service_id"])

        return "OK", 200, user_obj
    except Exception:
        traceback.print_exc()
        return INTERNAL_ERROR


def validate_user_api(
    api_token: str,
) -> Tuple[
    bool, str, int, Union[UserKontraktor, UserAlfa, UserRekanan, ServiceInternal, None]
]:
    """
    Validasi user BMT yang diambil melalui JWT (api key)
    """

    # get 'service_id' from jwt header
    try:
        jwt_header = jwt.get_unverified_header(api_token)
        cycle_type = jwt_header["ct"]
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return {"message": "Invalid token"}, 401, None
    except KeyError:
        return {"message": "missing required field for 'ct' on JWT header!"}, 400, None

    """
        Determine secret key based on cycle type:
            - sc: slow-cycle
            - fc: fast-cycle
    """
    if cycle_type == "sc":
        secret_key = Config.SECRET_KEY_SLOW_CYCLE
    elif cycle_type == "fc":
        secret_key = Config.SECRET_KEY_FAST_CYCLE

    # load and validate payload
    try:
        payload = jwt.decode(api_token, secret_key, algorithms=["HS256"])

        # validasi ulang header
        if jwt.get_unverified_header(api_token)["ct"] != cycle_type:
            raise jwt.InvalidTokenError
    except jwt.ExpiredSignatureError:
        return {"message": "token kadarluarsa!"}, 401, None
    except (jwt.InvalidTokenError, jwt.DecodeError):
        return {"message": "Invalid token"}, 401, None

    # validasi token untuk dev dan prod itu beda.
    token_env = payload.get("env", "dev")
    flask_env = getenv("bmt_env", "prod")
    if token_env != flask_env:
        return (
            {"message": f"Token hanya bisa dipakai di server {token_env} aja!"},
            401,
            None,
        )

    # load user
    try:
        user_type = payload["typ"]
        user_id = payload["id"]
    except KeyError as k:
        return (
            {"message": f"missing required field for {str(k)} on JWT payload!"},
            400,
            None,
        )

    if user_type in {"rekanan", "alfa", "kontraktor"}:
        return validate_user(user_id)
    elif user_type == "si":
        # si == Service Internal
        return validate_user_service_internal(service_id=user_id)
