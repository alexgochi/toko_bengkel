from applications.lib import PostgresDatabase

def get_data_merk():
    db = PostgresDatabase()
    query = """
        SELECT
            merk_id,
            merk_name
        FROM
            ms_merk
    """
    return db.execute(query)

def dt_data_category(search, offset):
    db = PostgresDatabase()
    query = """
        SELECT
            row_number() over (ORDER BY category_name) as no,
            mc.category_id,
            category_name,
            (select merk_name from ms_merk mm where mm.merk_id=mc.merk_id) merk_name,
            count(*) + 
                max(case when mp.category_id is null then -1 else 0 end)
            as jumlah_produk
        FROM ms_category mc
            LEFT JOIN ms_product mp on mc.category_id = mp.category_id
        WHERE
            category_name ILIKE %(search)s
        GROUP BY 
            mc.category_id,
            category_name
        ORDER BY 
            category_name;
    """
    param = {
        "search": f"%{search}%",
        "offset": offset
    }

    return db.execute_dt(query, param)


def update_data_category(data):
    db = PostgresDatabase()
    query = """
        UPDATE 
            ms_category
        SET
            merk_id = %(merk_id)s,
            category_name = %(category_name)s
        WHERE
            category_id = %(category_id)s
    """
    param = data

    return db.execute(query, param)

def delete_data_category(id):
    db = PostgresDatabase()
    query = """
        DELETE
        FROM 
            ms_category
        WHERE
            category_id = %(id)s
    """
    param = {
        "id" : id
    }

    return db.execute(query, param)

def add_data_category(data):
    db = PostgresDatabase()
    query = """
        INSERT INTO 
            ms_category 
                (merk_id, category_name) 
        VALUES 
                (%(merk_id)s, %(category_name)s);
    """
    param = data

    return db.execute(query, param)
