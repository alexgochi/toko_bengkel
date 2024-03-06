from application.lib import PostgresDatabase
from application.dao.master.masterUserDao import getMenu


def getDataMenuUserSAT(id_jabatan: str):
    return getMenu(id_jabatan)


def getDataUserSAT(nik):
    db = PostgresDatabase()
    query = """
        SELECT
            nik,
            nama_karyawan,
            kode_cabang,
            kode_jabatan,
            nama_jabatan,
            ms_karyawan.is_active
        FROM
            ms_karyawan
            INNER JOIN ms_store USING (kode_toko)
            INNER JOIN ms_jabatan USING (kode_jabatan)
        WHERE
            nik = %(nik)s;
    """
    param = {"nik": nik}

    return db.execute(query, param)


def getDataUserKontraktor(kode_kontraktor):
    db = PostgresDatabase()
    query = """
        SELECT
            mkt_kd_kontraktor kode_kontraktor,
            mkt_nama_kontraktor nama_kontraktor,
            mkt_nama_penanggung nama_penanggung,
            mkt_join_cabang list_cabang,
            mkt_status_kontraktor status
        FROM
            ms_kontraktor
        WHERE
            mkt_kd_kontraktor = %(kode_kontraktor)s;
    """
    param = {"kode_kontraktor": kode_kontraktor}

    return db.execute(query, param)


def getDataMenuUserKontraktor():
    db = PostgresDatabase()
    query = "SELECT get_menu_kontraktor() AS hasil;"

    return db.execute(query)


def get_data_user_rekanan(kode_rekanan: str):
    db = PostgresDatabase()
    query = """
        SELECT
            kode_rekanan,
            alias,
            is_b2b,
            need_validate,
            list_cabang,
            is_active
        FROM
            ms_rekanan2
        WHERE
            kode_rekanan = %(kode_rekanan)s;
    """
    param = {"kode_rekanan": kode_rekanan}

    return db.execute(query, param)


def get_data_user_service_internal(service_id: str):
    db = PostgresDatabase()
    query = """
        SELECT
            service_id,
            is_active
        FROM
            ms_service_internal
        WHERE
            service_id = %(service_id)s;
    """
    param = {"service_id": service_id}

    return db.execute(query, param)
