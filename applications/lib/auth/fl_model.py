from flask_login import UserMixin
from .fl_repository import getDataUserSAT, getDataUserKontraktor
import json


def json_default(obj):
    if isinstance(obj, set):
        return list(obj)

    return obj


class UserAlfa(UserMixin):
    def __init__(
        self, nik, nama, id_cabang, id_jabatan, nama_jabatan, menu, menu_role
    ) -> None:
        self.tipe_user = "alfa"

        # Nullish coalescing
        menu_role = menu_role or []
        menu = menu or []

        # '22115966'
        self.nik = nik.strip()
        # 'CANDRA WIJAYANTO'
        self.nama = nama.strip()
        # 'Z001'
        self.kode_cabang = id_cabang.strip()
        # 'C2517'
        self.kode_jabatan = id_jabatan.strip()
        # 'Website Programmer Analyst'
        self.nama_jabatan = nama_jabatan.strip()
        # contoh ada di repo
        self.menu = menu
        # NOTE: company_id sementara di hardcode
        self.company_id = "sat"
        # {'alfa', 'sat', 'Z001', 'C2517', 'admin_57', 'user_22', ...}
        self.roles = {
            self.tipe_user,
            self.company_id,
            self.kode_cabang,
            self.kode_jabatan,
            *menu_role,
        }

    def get_id(self) -> str:
        return self.nik

    def to_dict(self) -> dict:
        return {
            "nik": self.nik,
            "nama": self.nama,
            "kode_cabang": self.kode_cabang,
            "kode_jabatan": self.kode_jabatan,
            "nama_jabatan": self.nama_jabatan,
            "tipe_user": self.tipe_user,
            "company_id": self.company_id,
        }

    def to_json(self) -> str:
        # a = json.dumps(self.to_dict() | {"roles": self.roles}, default=json_default)
        # print(a)
        a = self.to_dict()
        a["roles"] = list(self.roles)

        # return json.dumps(self.to_dict() | {"roles": self.roles}, default=json_default)
        return json.dumps(a, default=json_default)

    def __str__(self) -> str:
        return str(self.to_dict())

    @property
    def is_active(self) -> bool:
        return True

        # sementara dimatikan ya ges
        hasil = getDataUserSAT(self.get_id())
        if hasil.is_error or hasil.is_empty:
            return False
        status = hasil.first["status"]

        # Y -> YES -> user aktif -> True
        # else -> NO -> user tidak aktif -> False
        return status == "Y"


class UserKontraktor(UserMixin):
    def __init__(
        self, kode_kontraktor, nama_kontraktor, nama_penanggung, list_cabang, menu
    ) -> None:
        self.tipe_user = "kontraktor"

        # 'SAT.BD.K.0009'
        self.kode_kontraktor = kode_kontraktor.strip()
        # 'PT. Mencari Cinta Sejati'
        self.nama_kontraktor = nama_kontraktor.strip()
        # 'Daniel Harliano Sitorus'
        self.nama_penanggung = nama_penanggung.strip()
        # ('KZ01', '1DZ1', 'EZ01', ...)
        self.list_cabang = tuple(list_cabang)
        # contoh ada di repo
        self.menu = menu
        # {'kontraktor'}
        self.roles = {"kontraktor"}

    def get_id(self) -> str:
        return self.kode_kontraktor

    def to_dict(self) -> dict:
        return {
            "tipe_user": self.tipe_user,
            "kode_kontraktor": self.kode_kontraktor,
            "nama_kontraktor": self.nama_kontraktor,
            "nama_penanggung": self.nama_penanggung,
            "list_cabang": self.list_cabang,
            "roles": self.roles,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    def __str__(self) -> str:
        return str(self.to_dict())

    @property
    def is_active(self) -> bool:
        return True

        # sementara dimantikan ya ges
        hasil = getDataUserKontraktor(self.get_id())
        if hasil.is_error or hasil.is_empty:
            return False
        status = hasil.first["status"]

        return status == "T"


class UserRekanan(UserMixin):
    def __init__(
        self,
        kode_rekanan: str,
        alias: str,
        is_b2b: bool,
        need_validate: bool,
        list_cabang: list,
    ) -> None:
        self.tipe_user = "rekanan"

        # SAT.R.0001
        self.kode_rekanan = kode_rekanan
        # Kanggo
        self.alias = alias
        # True / False
        self.is_b2b = is_b2b
        self.need_validate = need_validate
        # ('KZ01', 'TZ01', ...)
        self.list_cabang = tuple(list_cabang)

        # ['rekanan', 'SAT.R.0001', kanggo]
        self.roles = {self.tipe_user, self.kode_rekanan, self.alias}

    def get_id(self) -> str:
        return self.kode_rekanan

    def to_dict(self) -> dict:
        return {
            "tipe_user": self.tipe_user,
            "kode_rekanan": self.kode_rekanan,
            "nama_rekanan": self.nama_rekanan,
            "list_cabang": self.list_cabang,
            "roles": self.roles,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    def __str__(self) -> str:
        return str(self.to_dict())


class ServiceInternal(UserMixin):
    def __init__(self, service_id: str) -> None:
        self.tipe_user = "service_internal"

        # PAR, TAF, BMT, dll (buat sendiri bebas..)
        self.service_id = service_id

        # {"service_internal", "PAR", ...}
        self.roles = {self.tipe_user, self.service_id}

    def get_id(self) -> str:
        return self.service_id

    def to_dict(self) -> dict:
        return {
            "tipe_user": self.tipe_user,
            "service_id": self.service_id,
            "roles": self.roles,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), default=json_default)

    def __str__(self) -> str:
        return str(self.to_dict())
