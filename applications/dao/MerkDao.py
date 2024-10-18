from applications.lib import PostgresDatabase
from flask import jsonify

def get_data_category():
    db = PostgresDatabase()
    query = """
        SELECT
            category_id,
            category_name
        FROM
            ms_category
    """
    return db.execute(query)

def dt_data_merk(search, offset, orderBy):
    db = PostgresDatabase()
    query = f"""
        SELECT
            me.merk_id,
            merk_name,
            mc.category_name,
            mc.category_id,
            count(*)
                + max(case when mp.merk_id is null then -1 else 0 end)
            as jumlah_product
        FROM ms_merk me
        INNER JOIN ms_category mc on mc.category_id = me.category_id
        LEFT JOIN ms_product mp
            ON me.merk_id = mp.merk_id
        WHERE
            merk_name ILIKE %(search)s OR
            category_name ILIKE %(search)s
        GROUP BY
            me.merk_name,
            me.merk_id,
            category_name,
            mc.category_id
        ORDER BY
            {orderBy};
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param, limit=25)


def update_data_merk(data):
    db = PostgresDatabase()
    query = """
        SELECT merk_name
        FROM ms_merk
        WHERE LOWER(merk_name)= LOWER(%(merk_name)s)
        AND category_id= %(category_id)s
    """
    param = data
    res = db.execute(query, param)

    if res.result:
        return jsonify({"status": False, "message": "Nama Merk di Kategori tersebut sudah digunakan"})

    query = """
        UPDATE 
            ms_merk 
        SET 
            merk_name = %(merk_name)s,
            category_id = %(category_id)s 
        WHERE 
            merk_id = %(merk_id)s;
    """
    param = data
    res = db.execute(query, param)
    if res.is_error:
        return jsonify({"status": res.status, "message": str(res.pgerror)})
    return jsonify({"status": True, "message": "Berhasil Tambah data"})

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
        SELECT merk_name
        FROM ms_merk
        WHERE LOWER(merk_name)= LOWER(%(merk_name)s)
        AND category_id= %(category_id)s
    """
    param = data
    res = db.execute(query, param)

    if res.result:
        return jsonify({"status": False, "message": "Nama Merk di Kategori tersebut sudah digunakan"})

    query = """
        INSERT INTO 
            ms_merk 
                (merk_name, category_id) 
        VALUES 
                (%(merk_name)s, %(category_id)s);
    """
    param = data
    res = db.execute(query, param)
    if res.is_error:
        return jsonify({"status": res.status, "message": str(res.pgerror)})
    return jsonify({"status": True, "message": "Berhasil Tambah data"})


def get_all_category():
    db = PostgresDatabase()
    query = """
        SELECT
            merk_name kategori,
            mc.category_name merk,
            count(*)
                + max(case when mp.merk_id is null then -1 else 0 end)
            as jumlah_produk
        FROM ms_merk me
        INNER JOIN ms_category mc on mc.category_id = me.category_id
        LEFT JOIN ms_product mp
            ON me.merk_id = mp.merk_id
        GROUP BY
            me.merk_name,
            category_name
        ORDER BY
            me.merk_name
    """
    return db.execute(query)