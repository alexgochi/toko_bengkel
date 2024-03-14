from applications.lib import PostgresDatabase

def dt_data_merk(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            me.merk_id, 
            merk_name,
            count(*) 
                + max(case when mc.merk_id is null then -1 else 0 end) 
            as jumlah_category
        FROM ms_merk me
        LEFT JOIN ms_category mc 
            ON me.merk_id = mc.merk_id
        WHERE
            merk_name ILIKE %(search)s
        GROUP BY 
            me.merk_name, 
            me.merk_id
        ORDER BY 
            me.merk_name;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param)


def update_data_merk(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_merk 
        SET 
            merk_name = %(merk_name)s 
        WHERE 
            merk_id = %(merk_id)s;
    """
    param = data

    return db.execute(query, param)

def delete_data_merk(id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_merk
        WHERE
            merk_id = %(merk_id)s
    """
    param = {
        "merk_id" : id
    }

    return db.execute(query, param)

def add_data_merk(data):
    db = PostgresDatabase()
    query = """
        INSERT INTO 
            ms_merk 
                (merk_name) 
        VALUES 
                (%(merk_name)s);
    """
    param = data

    return db.execute(query, param)
