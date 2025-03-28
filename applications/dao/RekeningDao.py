from applications.lib import PostgresDatabase

def dt_data_rekening(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            rekening_id,
            rekening_no,
            rekening_name,
            rekening_bank,
            case when rekening_status is true Then 'Aktif'
            when rekening_status is false THEN 'Tidak Aktif' 
            END rekening_status
        FROM
            ms_rekening
        WHERE
            CAST(rekening_no AS TEXT) ILIKE %(search)s OR
            rekening_name ILIKE %(search)s OR
            rekening_bank ILIKE %(search)s
        ORDER BY
            rekening_id desc;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param, limit=50)

def get_data_rek_filter(search):
    db = PostgresDatabase()
    query = """
        SELECT
            rekening_id as "ID Rekening",
            rekening_no as "Nomor Rekening",
            rekening_name as "Nama Rekening",
            rekening_bank as "Nama Bank",
            case when rekening_status is true Then 'Aktif'
            when rekening_status is false THEN 'Tidak Aktif' 
            END as "Status Rekening"
        FROM
            ms_rekening
        WHERE
            CAST(rekening_no AS TEXT) ILIKE %(search)s OR
            rekening_name ILIKE %(search)s OR
            rekening_bank ILIKE %(search)s
        ORDER BY
            rekening_id;
    """
    param = {
        "search": f"%{search}%"
    }

    return db.execute(query, param)

def update_data_rekening(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_rekening
        SET
            rekening_no = %(rekening_no)s,
            rekening_name = %(rekening_name)s,
            rekening_bank = %(rekening_bank)s,
            rekening_status = %(rekening_status)s
        WHERE
            rekening_id = %(rekening_id)s
    """
    param = data

    return db.execute(query, param)

def delete_data_rekening(rekening_id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_rekening
        WHERE
            rekening_id = %(rekening_id)s
    """
    param = {
        "rekening_id" : rekening_id
    }

    return db.execute(query, param)

def add_data_rekening(data):
    db = PostgresDatabase()
    query = """
        INSERT INTO 
            ms_rekening 
                (rekening_no, rekening_name, rekening_status, rekening_bank) 
        VALUES 
                (%(rekening_no)s, %(rekening_name)s, %(rekening_status)s, %(rekening_bank)s);
    """
    param = data

    return db.execute(query, param)

def get_all_rek():
    db = PostgresDatabase()
    query = """
        SELECT
            rekening_no,
            rekening_name,
            rekening_bank,
            case when rekening_status is true Then 'Aktif'
            when rekening_status is false THEN 'Tidak Aktif' 
            END rekening_status
        FROM
            ms_rekening
        ORDER BY
            rekening_id desc;
    """
    return db.execute(query)