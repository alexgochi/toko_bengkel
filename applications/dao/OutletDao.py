from applications.lib import PostgresDatabase

def dt_data_outlet(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            outlet_id,
            outlet_name,
            outlet_address,
            outlet_phone,
            case when outlet_status is true Then 'Aktif'
            when outlet_status is false THEN 'Tidak Aktif' 
            END outlet_status
        FROM
            ms_outlet
        WHERE
            outlet_phone ILIKE %(search)s OR
            outlet_name ILIKE %(search)s OR
            outlet_address ILIKE %(search)s
        ORDER BY
            outlet_status asc;    
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param, limit=50)

def get_data_outlet_filter(search):
    db = PostgresDatabase()
    query = """
        SELECT
            outlet_id as "ID Outlet", 
            outlet_name as "Nama Outlet", 
            outlet_address as "Alamat Outlet", 
            outlet_phone as "Telepon Outlet",
            case when outlet_status is true Then 'Aktif'
            when outlet_status is false THEN 'Tidak Aktif' 
            END as "Status Outlet"
        FROM
            ms_outlet
        WHERE
            outlet_phone ILIKE %(search)s OR
            outlet_name ILIKE %(search)s OR
            outlet_address ILIKE %(search)s
    """
    param = {
        "search": f"%{search}%"
    }

    return db.execute(query, param)

def update_data_outlet(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_outlet
        SET
            outlet_name = %(outlet_name)s,
            outlet_address = %(outlet_address)s,
            outlet_phone = %(outlet_phone)s,
            outlet_status = %(outlet_status)s
        WHERE
            outlet_id = %(outlet_id)s
    """
    param = {
        "outlet_id" : data['outlet_id'],
        "outlet_address" : data['outlet_address'],
        "outlet_name" : data['outlet_name'],
        "outlet_phone" : data['outlet_phone'],
        "outlet_status" : data['outlet_status']
    }

    return db.execute(query, param)

def delete_data_outlet(outlet_id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_outlet
        WHERE
            outlet_id = %(outlet_id)s
    """
    param = {
        "outlet_id" : outlet_id
    }

    return db.execute(query, param)

def add_data_outlet(data):
    db = PostgresDatabase()
    query = """
        INSERT INTO 
            ms_outlet 
                (outlet_id, outlet_name, outlet_phone, outlet_address, outlet_status) 
        VALUES 
                (%(outlet_id)s, %(outlet_name)s, %(outlet_phone)s, %(outlet_address)s, %(outlet_status)s);
    """
    param = data

    return db.execute(query, param)

def check_id_outlet(outlet_id):
    db = PostgresDatabase()
    query = """
        SELECT
            outlet_id
        FROM
            ms_outlet
        WHERE
            outlet_id = %(outlet_id)s
    """
    param = {
        'outlet_id': outlet_id 
    }
    return db.execute(query, param)

def get_all_outlet():
    db = PostgresDatabase()
    query = """
        SELECT
            outlet_id,
            outlet_name,
            outlet_address,
            outlet_phone,
            case when outlet_status is true Then 'Aktif'
            when outlet_status is false THEN 'Tidak Aktif' 
            END outlet_status
        FROM
            ms_outlet
        ORDER BY
            outlet_status asc
    """
    return db.execute(query)