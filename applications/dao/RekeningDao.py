from applications.lib import PostgresDatabase

def dt_data_rekening(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            id,
            rek_no,
            rek_name,
            rek_bank,
            case when status is true Then 'Aktif'
            when status is false THEN 'Tidak Aktif' 
            END status
        FROM
            ms_rekening
        WHERE
            CAST(rek_no AS TEXT) ILIKE %(search)s OR
            rek_name ILIKE %(search)s OR
            rek_bank ILIKE %(search)s
        ORDER BY
            rek_bank;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param)


def update_data_rekening(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_rekening
        SET
            rek_no = %(rek_no)s,
            rek_name = %(rek_name)s,
            rek_bank = %(rek_bank)s,
            status = %(status)s
        WHERE
            id = %(id)s
    """
    param = {
        "rek_no" : data['rek_no'],
        "rek_name" : data['rek_name'],
        "rek_bank" : data['rek_bank'],
        "status" : data['status'],
        "id" : data['id']
    }

    return db.execute(query, param)

def delete_data_rekening(id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_rekening
        WHERE
            id = %(id)s
    """
    param = {
        "id" : id
    }

    return db.execute(query, param)

def add_data_rekening(data):
    db = PostgresDatabase()
    query = """
        INSERT INTO 
            ms_rekening 
                (rek_no, rek_name, status, rek_bank) 
        VALUES 
                (%(rek_no)s, %(rek_name)s, %(status)s, %(rek_bank)s);

    """
    param = data

    return db.execute(query, param)
